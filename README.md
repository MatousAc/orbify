# Orbify
## What is this? 

This is a small project aiming to simplify the process of transferring forms from **Integrify** to **Orbeon**. This process regularly involves a ton of clicking and reconfiguration of generic parameters. My aim is to reduce the time spent clicking time and allow the Workflow engineer to focus on translating any more-complicated logic/layout features between the platforms.  
Below I detail what exactly this tool can do for you, how to use it, along with some development notes.  

**Contents**  
[Download](#download)  
[Use](#use)  
[Capabilities](#capabilities)  
[Form Representation](#form-representation)  
[Development](#development)  
## Download
In order to run this script, you must
1. install Python 3.10.x or greater
2. get the python module pyperclip  
   `pip install pyperclip`
3. clone [this repository](git@github.com:MatousAc/orbify.git)
4. navigate into the repository
## Use

Orbify is designed to require minimal to use.  
1. copy the JSON you want translated to your clipboard
2. in the [orbify repository](.) run  
   `python orbify.py`
3.	enter the form's name (oddly, this *isn't* stored in the JSON)
4. resulting XForms source code is on the clipboard
## Capabilities
Orbify can translate most forms without a hitch. It translates the following fields without known bugs:
|Integrify|Orbeon|
|-|-|
|Short Text|text input|
|Long Text|text input|
|Search Box|text input|
|Hyperlink|text input|
|Rich Text|formatted text input|
|Number|number input, currency input|
|Email Address|email input|
|Contact Search|single select list with options populating from a resource|
|Calendar|date input|
|Radio Button|radio input/boolean input|
|Checkbox|multi-select checkboxes|
|Select List|static dropdown|
|File Attachment|file attachment |
|Password|secret input|
|Signature|handwritten signature|
|Image|blank space|
|Form Text|explanatory text|
|Blank Space|just a placeholder in the grid. no field associated|

There are special cases. When **currency** is detected, orbify translates the number field into a currency input.  
When a radio select has only yes and no options (or true/false), it is translated into a **boolean** input.  
**Images** get a placeholder, except for FTD Logo Images, which are common enough to hardcode and include.  
More similar additions will be added in the future (phone numbers, for instance).
## Form Representation

### **Integrify**
forms uses a purely JSON representation to keep track of their forms. There isn't much complexity to their setup, but basically the JSON is:  
*json representation* | **code representation**
* a list of *objects* 
* each object is a **section**, the building block of a form 
* each section's contents list contains **container** *objects* 
* a container has columns in which all *items*/**fields** reside 
* if there are two objects in the column list, then this container is 2-columned. if there's one, then it's just a single column (common sense)
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
Note that Integrify's JSON notation does not contain the name of the form itself, so this is gathered at runtime.

### **Orbeon**
uses XForms to represent its forms. XForms is an XML-style representation that leverages the MVC approach.  
The **model** describes the form data and sets up constraints and submissions.  
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

Next is the xf:bind section, so I'll call this the "bind." It generically starts with
~~~
<xf:bind id="fr-form-binds" ref="instance('fr-form-instance')"> 
~~~
Inside this are tags that, again, mirror the form structure, except this time they only include form fields and "bind" the control names to a "name," "ref," and "type." The tag format is as follows:
~~~
<xf:bind id="control_name-bind" ref="control_name" name="control_name" type="xf:datatype"/> 
~~~
Where datatype can be Boolean, anyURI, date, etc. Fields such as radio buttons, checkboxes, or dropdowns are no different from text fields with regards to how they store data, so datatype isn't specified for them here. They are just text in the background. In our program, however, they will each definitely have their own representation. 

The datatype is optional and not included in section or grid tags. Basic text inputs don't indicate a datatype, but typically include an xxf:whitespace="trim" attribute. 

The currency datatype seems to be denoted by 

type="xf:decimal" 

constraint="xxf:fraction-digits(2)" 

Also, this is where other data attributes such as required and relevant (visible?) go. 

 

Next there is another instance tag this time of the form: 

<xf:instance id="fr-form-metadata" xxf:readonly="true" xxf:exclude-result-prefixes="#all"> 

This appears to provide metadata about the form and doesn't look hard to make. Orbify needs the form title and can fill out basic metadata, standard control_name, description (empty), created/updated software versions, etc. It's cookie-cutter enough to be easy I think. 

 

Next is the form attachments instance tag. It appears to be invariable empty regardless of what attachments. All it is is: 

<xf:instance id="fr-form-attachments" xxf:exclude-result-prefixes="#all"> 

<attachments/> 

</xf:instance> 

 

The final piece of the model is the "resources." This section seems to keep static data for the form that is only "for display." we have the following tags: 

<xf:instance xxf:readonly="true" id="fr-form-resources" xxf:exclude-result-prefixes="#all"> 

<resources> 

<resource xml:lang="en"> 

Following this are tags for each piece of data in the form: 

<control_name> 

<label>Control Name</label> 

<hint/> 

</control_name> 

Within radio buttons/checkboxes, the options are items in the resources section (since the submitted data is same as a basic input). 

<item> 

<label>Option</label> 

<hint/> 

<value>option</value> 

</item> 

Clearly, this is easily programmable with the available data. 

After this instance, the XForms model and head tags close. 

 

View 

This section begins with the generic nested tags 

<xh:body> 

<fr:view> 

<fr:body xmlns:xbl="http://www.w3.org/ns/xbl" xmlns:p="http://www.orbeon.com/oxf/pipeline" xmlns:oxf="http://www.orbeon.com/oxf/processors"> 

 

Within this there are tags for every section of the form:  

<fr:section id="control_name-section" bind="control_name-bind"> 

And every grid in the same format. Inside is likely the most difficult part of Orbify. Every data field is contained within an fr:c tag. This tag seems to place data fields within the grid. The format is 

<fr:c x="#" y="#" w="#"> 

It appears that XForms has borrowed a bootstrap-style grid scheme. 

The simplest variable above is w which is obviously the element's width. It can range from 1-12. A full-width element is w="12" and one that takes up half a page is w="6". 

Next, the x and y variables seem to indicate position on the page relative to the top left corner of the grid. Here is an example of what all these values look like: 

 
 

Within these tags is all the rest of the field's information. The first tag specifies type of viewed field it is. Known types are: 

input 

date 

attachment 

yesno-input 

select 

select1 

currency 

 

These may include an id, bind, class, and other attributes. 

Subtags include 

label 

hint 

alert 

itemset (for select/select1) 

 

 

## Development 

Head text 

 

 