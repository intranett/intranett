<?xml version="1.0"?>
<object name="Contract" meta_type="Factory-based Type Information"
   xmlns:i18n="http://xml.zope.org/namespaces/i18n">
 <property name="title">Contract</property>
 <property name="description">A Jarn Contract</property>
 <property name="content_icon">document.gif</property>
 <property name="content_meta_type">Contract</property>
 <property name="product">jarn.extranet</property>
 <property name="factory">addContract</property>
 <property name="immediate_view">base_edit</property>
 <property name="global_allow">False</property>
 <property name="filter_content_types">False</property>
 <property name="allowed_content_types">
  <element value="Person"/>
 </property>
 <property name="allow_discussion">False</property>
 <alias from="(Default)" to="base_view"/>
 <alias from="edit" to="base_edit"/>
 <action title="View" action_id="view" category="object" condition_expr=""
    url_expr="string:${object_url}/base_view" visible="True">
  <permission value="View"/>
 </action>
 <action title="Edit" action_id="edit" category="object" condition_expr=""
    url_expr="string:${object_url}/base_edit" visible="True">
  <permission value="Modify portal content"/>
 </action>
</object>