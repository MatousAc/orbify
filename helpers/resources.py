# long predefined strings that are used in 
# generating the source code string 

htmlAttrs = """xmlns:xh="http://www.w3.org/1999/xhtml" 
xmlns:xf="http://www.w3.org/2002/xforms"
xmlns:xs="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:ev="http://www.w3.org/2001/xml-events"
xmlns:xi="http://www.w3.org/2001/XInclude"
xmlns:xxi="http://orbeon.org/oxf/xml/xinclude"
xmlns:xxf="http://orbeon.org/oxf/xml/xforms"
xmlns:map="http://www.w3.org/2005/xpath-functions/map"
xmlns:array="http://www.w3.org/2005/xpath-functions/array"
xmlns:exf="http://www.exforms.org/exf/1-0"
xmlns:fr="http://orbeon.org/oxf/xml/form-runner"
xmlns:saxon="http://saxon.sf.net/"
xmlns:sql="http://orbeon.org/oxf/xml/sql"
xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:fb="http://orbeon.org/oxf/xml/form-builder"
fr:data-format-version="4.0.0\""""
modelAttrs = 'id="fr-form-model" xxf:expose-xpath-types="true" xxf:analysis.calculate="true"'
modelDataMapAttrs = 'id="fr-form-instance" xxf:exclude-result-prefixes="#all" xxf:index="id"'
modelBindAttrs = """id="fr-form-binds" ref="instance('fr-form-instance')\""""
modelMetaAttrs = 'id="fr-form-metadata" xxf:readonly="true" xxf:exclude-result-prefixes="#all"'
modelAttachAttrs = 'id="fr-form-attachments" xxf:exclude-result-prefixes="#all"'
modelResourcesAttrs = 'xxf:readonly="true" id="fr-form-resources" xxf:exclude-result-prefixes="#all"'
