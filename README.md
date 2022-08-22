# **Orbify**
**Contents** | [Overview](#overview) | [Download](#download) | [Use](#use) | [Capabilities](#capabilities) | [Form Representation](#form-representation) | [Program](#program)
## Overview
This is a small project aiming to simplify the process of transferring forms from **Integrify** to **Orbeon**. Because this process regularly involves much clicking, copying, pasting, and reconfiguration of generic parameters, orbify reduces this waste of time and allows Workflow Engineers to focus on translating the more-complicated logic/layout features between the platforms.  
Below I detail what exactly this tool can do for you, and how to use it, along with some development notes.  
Note, the program is specialized for FTD Solutions, but can be quite easily altered for other projects. A more generic version will come eventually in another branch.  

## Download
In order to run this script, you must
1. install Python 3.10.x or greater
2. get the python module pyperclip. use:  
   `pip install pyperclip`
3. clone [this repository](git@github.com:MatousAc/orbify.git)
## Use

Orbify is designed to require minimal effort to use.  
1. navigate into the orbify repository on any CLI
2. copy the JSON you want translated to your clipboard.  
   it now suffices to hit `Ctrl + A, Ctrl + C` (while in Integrify's **View JSON**) to select and copy all the JSON because the extra text that is copied along with the JSON is ignored by Orbify.
3. in the [orbify repository](.) run  
   `python orbify.py`
4. enter the form's name (oddly, this *isn't* stored in the JSON) and hit `Enter`
5. the XForms source code is on your clipboard and control names for all data fields are printed out below
## Capabilities
**Layout**: Just about all pieces of the layout are translated. The only significant difference is that in integrify there are columns inside containers, while Orbeon's grids have uniform columns *and rows*. This can cause some minor horizontal misalignments which can be adjusted by hand.
|Integrify|Orbeon|
|-|-|
|section|section|
|container|grid|
|column|place <fr:c/>|
|field|field|

**Fields**: Orbify translates the following fields without known bugs:
|Integrify|Orbeon|
|-|-|
|short text|text input|
|long text|text area|
|search box|text input or static select with service and action (FTD API)|
|hyperlink|text input with link regex|
|rich text|formatted text input|
|number|number input or currency input if currency detected|
|email address|email input|
|contact search|static select with service and action using FTD API|
|calendar|date input|
|radio button|radio input|
|checkbox|multi-select checkboxes|
|select list|static dropdown or static select with service and action (FTD API)|
|(multi) file attachment|file attachment (multi is not available in Orbeon PE 2019|
|password|secret input|
|signature|handwritten signature|
|form text|explanatory text|
|horizontal line|explanatory text containing \<hr/> tag|
|image|blank space $\downarrow$|
|blank space|just a placeholder in the grid. no field associated|

There are special cases:  
* When a radio select or checkbox input has only the options "yes" and "no" (or true/false, case insensitive), it is translated into a **boolean** input, known as YesNo in Orbeon.  
* **Images** get a placeholder, except for **FTD Logo Images**, which are common enough in FTD forms to hardcode and include.  
* **Phone numbers** are detected based on field labels ("Cell Phone", "Phone #", "Work Phone", etc . . .) and are translated into text inputs with special phone-number-like constraints and rigid formatting.  
* **Grid** translation is not currently supported. Grids are replaced with blank spaces.

**Field Attributes**
|Integrify|Orbeon|Supported?|
|-|-|-|
|required|required|$\checkmark$|
|readonly|readonly|$\checkmark$|
|hidden|visibility/relevant|$\checkmark$|
|digits-after-decimal|digitsAfterDecimal|$\checkmark$|
|show|visibility/relevant|X|
|Allowed File Types|Supported Mime Types|X|

## Form Representation
This section simply explains how forms are represented in both of the two systems.
### **Integrify**
forms uses a purely JSON representation to keep track of their forms. There isn't much complexity to their setup. Below, it is hierarchically broken down with the *json representation* italicized and the **logical/code representation** emboldened:
* The JSON from Integrify is a list of *objects* 
* each object is a **section**, the building block of a form 
* each section's contents list contains **container** *objects* 
* a container has columns in which all *item objects*/**fields** reside 
* if there are *two objects* in the column list, then this **container is 2-columned**. if there's one, then it's just a single column (common sense)
* each item at this level corresponds to a field in the form
* fields are *objects* that contain the field's attributes. these attributes include things like 
	* QuestionType (ShortText, FileAttatchment) 
	* Label (Job Title, Acceptance Letter) 
	* Class (for CSS) 
	* show 
	* isdirty 
	* id 
	* validation {required, minMessage, . . .} 

There are structures (such as sections, and columns) and attributes (Label, show, validation) that we need to retain, and others we won't really care to try to translate. Some fields for Orbeon are calculated (any control name can be easily based on "Label" or element count).  
Note that Integrify's JSON notation does not contain the name of the form itself, so this is collected at runtime.

### **Orbeon**
uses XForms to represent its forms. XForms is an XML-style representation that leverages the MVC approach.  
The **model** describes the form data and sets up constraints, submission-types, API calls, and form resources.  
The **view** describes what controls appear in the form, how they are grouped together, and what data they are bound to. 

The very first tag is the xh:html tag, containing various imports from w3, Orbeon, and Saxon. This first tag is just about identical in each form andis handled using a simple string in Python.  
To a high degree, all of the following sections mirror the form structure. The model primarily deals with data and data-binding, while the view will deal a lot more with placement and such.

#### **Model**
The model is contained inside the head tag alongside a title (I think there can be more than one model per document). The model contains **instances** which are basically groupings of different types of information about all elements in the form.  
There are five instances: control names, bindings, metadata, attachments, and resources.  
The first "instance" contains a self-closing tag for all the forms "control names"  
~~~
<control_name/>
~~~
except form images and attachment fields include more information in their tags.  
We start with the generic 
~~~
<xf:instance id="fr-form-instance" xxf:exclude-result-prefixes="#all" xxf:index="id"> 
~~~
on the outside, and then the hierarchy is as follows:  
xf:Instance > form > section_control > grid_control > field_control 

Next is the xf:**bind** section, so I'll call this the "bind." It generically starts with
~~~
<xf:bind id="fr-form-binds" ref="instance('fr-form-instance')"> 
~~~
Inside this are tags that, again, mirror the form structure, except this time they only include form fields and "bind" the control names to a "name," "ref," and "type." The tag format is as follows:
~~~
<xf:bind id="control_name-bind" ref="control_name" name="control_name" type="xf:datatype"/> 
~~~
where `datatype` can be boolean, anyURI, date, decimal, etc. Fields such as radio buttons, checkboxes, or dropdowns are no different from text fields with regards to how they store data, so datatype isn't specified for them here. They are just text in the background. In our program, however, they will each definitely have their own representation.  
The datatype is optional and not included in section or grid tags. Basic text input don't indicate a datatype, but typically include an xxf:whitespace="trim" attribute.  
Constraints can also be set here. For instance, the currency datatype seems to be denoted by `type="xf:decimal" constraint="xxf:fraction-digits(2)"`. Also, this is where other data attributes such as required and relevant (visible?) may go. 

Next there is another instance tag this time of the form:
~~~
<xf:instance id="fr-form-metadata" xxf:readonly="true" xxf:exclude-result-prefixes="#all"> 
~~~
This appears to provide **metadata** about the form and isn't difficult to generate as it's layout is completely static.
The form **attachments** instance tag, likewise, appears to be simple. It is invariably empty regardless of what attachments may be in the form.
~~~
<xf:instance id="fr-form-attachments" xxf:exclude-result-prefixes="#all">
	<attachments/> 
</xf:instance>
~~~

The final piece of the model is the **resources** instance. This section seems to keep static data for the form that is only "for display" including form text, and checkbox/radio options. We have the following tags: 
~~~
<xf:instance xxf:readonly="true" id="fr-form-resources" xxf:exclude-result-prefixes="#all"> 
	<resources>
		<resource xml:lang="en"> 
~~~
Following this are tags for each piece of data in the form:
~~~
<control_name>
	<label>Control Name</label>
	<hint/>
</control_name> 
~~~
Inputs with choices, such as radio buttons and checkboxes, have items in the resources section:
~~~
<item>
	<label>Option</label>
	<hint/>
	<value>option</value>
</item>
~~~
After this instance, the XForms model and head tags close.

### **View**
This section begins with the generic nested tags 
~~~
<xh:body>
	<fr:view>
		<fr:body xmlns:xbl="http://www.w3.org/ns/xbl" xmlns:p="http://www.orbeon.com/oxf/pipeline" xmlns:oxf="http://www.orbeon.com/oxf/processors"> 
~~~

Within this there are tags for every section of the form:
~~~
<fr:section id="control_name-section" bind="control_name-bind"> 
~~~
and every grid in the same format. Every data field is contained within an fr:c tag. This tag places data fields within the grid. The format is:
~~~
<fr:c x="#" y="#" w="#" h="#"> 
~~~
It appears that XForms has borrowed a bootstrap-style grid scheme (or the other way around).

$w$ which is obviously the element's width. It can range from 1-12. A full-width element is w="12" and one that takes up half a page is $w="6"$. Height $h$ doesn't seem to have a limit. The $x$ and $y$ variables seem to indicate position on the page relative to the top left corner of the grid. Here is an example of what all these values look like: 

## Program
Form translation is orchestrated in [orbify.py](orbify.py).
1. First the form's name is collected and the JSON is extracted from whatever is on the clipboard
   ~~~
	 name = input("Form Name: ")
	 src = extractJSON(pyperclip.paste())
	 src = json.loads(src)
	 ~~~
2. Next, the form object is created.
   ~~~
	 form = Form(name, src)
   ~~~
	 JSON is retrieved from the clipboard and parsed. Then the form creates section objects, with in turn create grids, and so on and so forth. Each form "block" contains objects within it that are iteratively constructed using parsed JSON objects.  
	 Eventually, we have `Form` > `Section` > `Grid` > `Place` - `Field` where each level block contains multiple smaller blocks except each place contains only one field.  
	 This might feel like overkill, but it is actually a very useful and scalable code representation for continuous development.
3. The second line of code
   ~~~
	 result = gen_xhtml(form)
	 ~~~
	 constructs a string with all the XML/XForms source code in it. From a developer's perspective, one would hope to have all the code that generates the model's *resources* in one place, while code that generates the *view* would be elsewhere. Although there are other ways to organize (possibly by field and class type, because of the hierarchical nature of XML, I chose to use the **visitor design pattern**.  
	 This is a slightly more complex programming paradigm, so I won't explain it here, but it's proved to work extremely well for this use case.
3. Finally,
   ~~~
	 for cn in fieldControls:
		print(cn)
	 ~~~
	 prints out all the data field's control names and
   ~~~
	 pyperclip.copy(result)
	 ~~~
	 places the source code for the form on your clipboard - ready to paste into Orbeon.
