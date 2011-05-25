from zope.interface import Interface
from zope.interface import implements
from DateTime import DateTime
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Extropy.config import TIMETOOLNAME
from Products.Archetypes.utils import OrderedDict


class IWorkLogView(Interface):
    def activity(period=None, people="all", group_by="day", start=None):
        """Return a grouped list of work activity.
        """

    def people():
        """Return a dictionary with all people.

        This is returned as a list of (userid, full name) tuples.
        """


def DateToPeriod(period="week", date=None):
    """Return the start and end dates for a time period defined by a
    length and a date.
    """

    if date is None:
        date=DateTime()

    if period=="day":
        start=date.earliestTime()
        end=date.latestTime()
    elif period=="week":
        start=(date-((date.dow()+6)%7)).earliestTime()
        end=(start+6).latestTime()
    elif period=="month":
        start=(date-(date.day()-1)).earliestTime()
        end=(start+31).latestTime()
        if end.day()<28:
            end-=end.day()
    else:
        raise ValueError("undefined period")

    return (start, end)


class WorkLogView(BrowserView):
    implements(IWorkLogView)

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.mt=getToolByName(self.context, "portal_membership")
        self.tool=getToolByName(self.context, TIMETOOLNAME)

        self.period=self.request.get("period", "week")
        self.person=self.request.get("person", "all")
        self.group_by=self.request.get("group_by", "day")
        self.today=DateTime()
        start = self.request.get("start")
        if start is not None:
            start = DateTime(start)
        else:
            start = DateTime()
        (self.start, self.end)=DateToPeriod(period=self.period, date=start)

    def getMemberName(self, userid):
        member=self.mt.getMemberById(userid)
        if member is None:
            return userid

        name=member.getProperty("fullname")
        return name and name or userid

    def summarize(self, bookings):
        return dict(hours=sum((booking["hours"] for booking in bookings)))

    def MorphHourBrain(self, brain):
        obj = brain.getObject()
        author = brain.Creator

        chain=[dict(url=link.absolute_url(), title=link.Title())
                for link in obj.getExtropyParentChain(True)]
        chain.reverse()

        return dict(
                userid=author,
                fullname=self.getMemberName(author),
                creator=brain.Creator,
                hours=obj.workedHours(),
                title=brain.Title,
                start=obj.start(),
                end=obj.end(),
                summary=obj.getSummary(),
                url=brain.getURL(),
                chain=chain,
                )

    def activity(self):
        query=dict(
                path="/".join(self.context.getPhysicalPath()),
                start=dict(query=[self.start, self.end], range="minmax"),
                portal_type="ExtropyHours",
                sort_on="start",
                sort_order="descending")

        if self.person!="all":
            query["Creator"]=self.person

        data=[self.MorphHourBrain(brain) for brain in self.tool(query)]

        grouping = dict(project=lambda x: x["chain"][0]["title"],
                        person=lambda x: x["fullname"],
                        day=lambda x: x["start"].earliestTime(),
                        )

        results=OrderedDict()
        keyfunc=grouping.get(self.group_by, grouping["day"])
        for booking in data:
            key=keyfunc(booking)
            if key not in results:
                results[key]=[]
            results[key].append(booking)

        results=[dict(title=key, summary=self.summarize(value), bookings=value)
                        for (key, value) in results.items()]
        if self.group_by != "day":
            results.sort(key=lambda x: x["title"])

        return results

    def people(self):
        people=self.tool.Indexes["Creator"].uniqueValues()
        creators=[(userid, self.getMemberName(userid)) for userid in people]
        creators.sort(key=lambda x: x[1])
        creators.insert(0, ("all", "Everyone"))
        return creators
