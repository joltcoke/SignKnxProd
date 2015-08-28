import xml.etree.ElementTree as ET

manufacturerId = "M-00A6"
catalogNumber = "6"
catalogItemNumber = "2"
serialNumber = "00000004"
versionNumber = "4"
orderNumber = "00001153"
applicationNumber = "4"
applicationVersion = "2"

# "M-00A6_CS-4"
catalogSectionId = manufacturerId + "_CS-" + catalogNumber
# "M-00A6_H-00000003-1"
hardwareId = manufacturerId + "_H-" + serialNumber + "-" + versionNumber
# "M-00A6_H-00000003-1_P-00001152"
productId= hardwareId + "_P-" + orderNumber
# "M-00A6_H-00000003-1_HP-0003-00-0FC5"
hardware2ProgramId = hardwareId + "_HP-" + "%04X" % int(applicationNumber) + "-" + "%02X" % int(applicationVersion) + "-0FC5"
# "M-00A6_A-0003-00-0FC5"
applicationProgramId = manufacturerId + "_A-" + "%04X" % int(applicationNumber) + "-" + "%02X" % int(applicationVersion) + "-0FC5"
# "M-00A6_H-00000003-1_HP-0003-00-0FC5_CI-00001152-1"
catalogItemId = hardware2ProgramId + "_CI-" + orderNumber + "-" + catalogItemNumber

def indent(elem, level=0):
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

def addTranslations(languagesXML, itemsXML, refId, tagName):
	for itemXML in itemsXML:
		countryCode = itemXML.get("{http://www.w3.org/XML/1998/namespace}lang")
		translation = itemXML.text

		languageXML = languagesXML.find("*[@Identifier='" + countryCode + "']")
		
		if languageXML is None:
			languageXML = ET.SubElement(languagesXML, "Language")
			languageXML.set("Identifier", countryCode)

		translationUnitXML = languageXML.find("*[@RefId='" + refId + "']")
	
		if translationUnitXML is None:
			translationUnitXML = ET.SubElement(languageXML, "TranslationUnit")
			translationUnitXML.set("RefId", refId)
	
		translationElementXML = translationUnitXML.find("*[@RefId='" + refId + "']")

		if translationElementXML is None:
			translationElementXML = ET.SubElement(translationUnitXML, "TranslationElement")
			translationElementXML.set("RefId", refId)
	
		translationXML = ET.SubElement(translationElementXML, "Translation")
		translationXML.set("AttributeName", tagName)
		translationXML.set("Text", translation)

	return

def createRootNode():
	rootXML = ET.Element("KNX")

	rootXML.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
	rootXML.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
	rootXML.set("CreatedBy", "knxconv")
	rootXML.set("ToolVersion", "4.0.1907.45562")
	rootXML.set("xmlns", "http://knx.org/xml/project/11")

	return rootXML

def createCatalog(srcRootXML):
	languagesXML = ET.Element("Languages")
	srcDeviceXML = srcRootXML.find("info")
	dstRootXML = createRootNode()

	manufacturerDataXML = ET.SubElement(dstRootXML, "ManufacturerData")

	manufacturerXML = ET.SubElement(manufacturerDataXML, "Manufacturer")
	manufacturerXML.set("RefId", manufacturerId)

	catalogXML = ET.SubElement(manufacturerXML, "Catalog")

	catalogSectionXML = ET.SubElement(catalogXML, "CatalogSection")
	catalogSectionXML.set("Id", catalogSectionId)
	catalogSectionXML.set("Name", "Power Supplies")
	addTranslations(languagesXML, srcDeviceXML.findall("category"), catalogSectionId, "Name")
	catalogSectionXML.set("Number", catalogNumber)
	catalogSectionXML.set("VisibleDescription", "")
	catalogSectionXML.set("DefaultLanguage", "de-DE")
	catalogSectionXML.set("NonRegRelevantDataVersion", "0")

	catalogItemXML = ET.SubElement(catalogSectionXML, "CatalogItem")
	catalogItemXML.set("Id", catalogItemId)
	catalogItemXML.set("Name", "KNX-Netzteil2")
	addTranslations(languagesXML, srcDeviceXML.findall("name"), catalogSectionId, "Name")
	catalogItemXML.set("Number", catalogItemNumber)
	# According to spec: VisibleDescription. Missing?
	catalogItemXML.set("ProductRefId", productId)
	catalogItemXML.set("Hardware2ProgramRefId", hardware2ProgramId)
	catalogItemXML.set("DefaultLanguage", "de-DE")
	catalogItemXML.set("NonRegRelevantDataVersion", "0")

	manufacturerXML.append(languagesXML)

	return dstRootXML

def createHardware(srcRootXML):
	languagesXML = ET.Element("Languages")
	srcDeviceXML = srcRootXML.find("info")
	dstRootXML = createRootNode()
	
	manufacturerDataXML = ET.SubElement(dstRootXML, "ManufacturerData")
	
	manufacturerXML = ET.SubElement(manufacturerDataXML, "Manufacturer")
	manufacturerXML.set("RefId", manufacturerId)

	hardwaresXML = ET.SubElement(manufacturerXML, "Hardware")

	hardwareXML = ET.SubElement(hardwaresXML, "Hardware")
	hardwareXML.set("Id", hardwareId)
	hardwareXML.set("Name", "KNX-Netzteil")
	hardwareXML.set("SerialNumber", serialNumber)
	hardwareXML.set("VersionNumber", versionNumber)
	# According to spec: Bus Current. Missing?
	hardwareXML.set("IsAccessory", "0")
	hardwareXML.set("HasIndividualAddress", "1")
	hardwareXML.set("HasApplicationProgram", "1")
	# According to spec: Download Application Program. Missing?
	hardwareXML.set("HasApplicationProgram2", "0")
	# According to spec: Download Application Program2. Missing?
	hardwareXML.set("IsPowerSupply", "0")
	hardwareXML.set("IsChoke", "0")
	hardwareXML.set("IsCoupler", "0")
	hardwareXML.set("IsPowerLineRepeater", "0")
	hardwareXML.set("IsPowerLineSignalFilter", "0")
	hardwareXML.set("IsCable", "0")
	hardwareXML.set("NonRegRelevantDataVersion", "0")
	hardwareXML.set("IsIPEnabled", "0")

	productsXML = ET.SubElement(hardwareXML, "Products")

	productXML = ET.SubElement(productsXML, "Product")
	productXML.set("Id", productId)
	productXML.set("Text", "KNX-Netzteil")
	addTranslations(languagesXML, srcDeviceXML.findall("name"), catalogSectionId, "Name")
	productXML.set("OrderNumber", orderNumber)
	productXML.set("IsRailMounted", "1")
	productXML.set("WidthInMillimeter", "1.0500000e+002")
	productXML.set("VisibleDescription", "KNX-Netzteil")
	addTranslations(languagesXML, srcDeviceXML.findall("name"), catalogSectionId, "VisibleDescription")
	productXML.set("DefaultLanguage", "de-DE")
	productXML.set("Hash", "")
	productXML.set("NonRegRelevantDataVersion", "0")

	registrationInfoXML = ET.SubElement(productXML, "RegistrationInfo")
	registrationInfoXML.set("RegistrationStatus", "Registered")
	registrationInfoXML.set("RegistrationSignature", "")
		
	hardware2ProgramsXML = ET.SubElement(hardwareXML, "Hardware2Programs")

	hardware2ProgramXML = ET.SubElement(hardware2ProgramsXML, "Hardware2Program")
	hardware2ProgramXML.set("Id", hardware2ProgramId)
	hardware2ProgramXML.set("MediumTypes", "MT-0")
	hardware2ProgramXML.set("Hash", "")

	applicationProgramRefXML = ET.SubElement(hardware2ProgramXML, "ApplicationProgramRef")
	applicationProgramRefXML.set("RefId", applicationProgramId)

	# According to spec: Application Program 2 Ref. Missing?

	registrationInfoXML = ET.SubElement(hardware2ProgramXML, "RegistrationInfo")
	registrationInfoXML.set("RegistrationStatus", "Registered")
	registrationInfoXML.set("RegistrationSignature", "")

	manufacturerXML.append(languagesXML)

	return dstRootXML

def createProduct(srcRootXML):
	dstRootXML = createRootNode()
	
	manufacturerDataXML = ET.SubElement(dstRootXML, "ManufacturerData")
	
	manufacturerXML = ET.SubElement(manufacturerDataXML, "Manufacturer")
	manufacturerXML.set("RefId", manufacturerId)
	
	applicationProgramsXML = ET.SubElement(manufacturerXML, "ApplicationPrograms")

	applicationProgramXML = ET.SubElement(applicationProgramsXML, "ApplicationProgram")
	applicationProgramXML.set("Id", applicationProgramId)
	applicationProgramXML.set("ApplicationNumber", applicationNumber)
	applicationProgramXML.set("ApplicationVersion", applicationVersion)
	applicationProgramXML.set("ProgramType", "ApplicationProgram")
	applicationProgramXML.set("MaskVersion", "MV-0705")
	# According to spec: Visible Description. Missing?
	applicationProgramXML.set("Name", "KNX-Netzteil")
	applicationProgramXML.set("LoadProcedureStyle", "DefaultProcedure")
	applicationProgramXML.set("PeiType", "0")
	# According to spec: Serial Number. Missing?
	# According to spec: Help Topic ID. Missing?
	applicationProgramXML.set("HelpFile", "")
	applicationProgramXML.set("DefaultLanguage", "de-DE")
	applicationProgramXML.set("DynamicTableManagement", "0")
	applicationProgramXML.set("Linkable", "0")
	applicationProgramXML.set("MinEtsVersion", "4.0")
	applicationProgramXML.set("PreEts4Style", "0")
	applicationProgramXML.set("NonRegRelevantDataVersion", "0")
	# According to spec: Replaces Versions. Missing?
	applicationProgramXML.set("Hash", "")
	# Not in spec. Obsolete? applicationProgramXML.set("ConvertedFromPreEts4Data", "1")
	# Not in spec. Obsolete? applicationProgramXML.set("Broken", "0")
	applicationProgramXML.set("IPConfig", "Tool")
	applicationProgramXML.set("AdditionalAddressesCount", "0")
	# Not in spec. Obsolete? applicationProgramXML.set("DownloadInfoIncomplete", "0")
	# Not in spec. Obsolete? applicationProgramXML.set("CreatedFromLegacySchemaVersion", "0")

	staticXML = ET.SubElement(applicationProgramXML, "Static")

	codeXML = ET.SubElement(staticXML, "Code")

	absoluteSegmentAddr = "16384"
	absoluteSegmentId = applicationProgramId + "_AS-" + "%04X" % int(absoluteSegmentAddr)
	absoluteSegmentXML = ET.SubElement(codeXML, "AbsoluteSegment")
	absoluteSegmentXML.set("Id", absoluteSegmentId)
	absoluteSegmentXML.set("Address", absoluteSegmentAddr)
	absoluteSegmentXML.set("Size", "403")
	absoluteSegmentXML.set("UserMemory", "0")

	absoluteSegmentAddr = "16787"
	absoluteSegmentId = applicationProgramId + "_AS-" + "%04X" % int(absoluteSegmentAddr)
	absoluteSegmentXML = ET.SubElement(codeXML, "AbsoluteSegment")
	absoluteSegmentXML.set("Id", absoluteSegmentId)
	absoluteSegmentXML.set("Address", absoluteSegmentAddr)
	absoluteSegmentXML.set("Size", "401")
	absoluteSegmentXML.set("UserMemory", "0")

	absoluteSegmentAddr = "17188"
	absoluteSegmentId = applicationProgramId + "_AS-" + "%04X" % int(absoluteSegmentAddr)
	absoluteSegmentXML = ET.SubElement(codeXML, "AbsoluteSegment")
	absoluteSegmentXML.set("Id", absoluteSegmentId)
	absoluteSegmentXML.set("Address", absoluteSegmentAddr)
	absoluteSegmentXML.set("Size", "360")
	absoluteSegmentXML.set("UserMemory", "0")

	#dataXML = ET.SubElement(absoluteSegmentXML, "Data")
	#dataXML.text = ""

	#maskXML = ET.SubElement(absoluteSegmentXML, "Mask")
	#maskXML.text = ""

	parameterTypesXML = ET.SubElement(staticXML, "ParameterTypes")

	parameterTypeName = "TestParType"
	parameterTypeId = applicationProgramId + "_PT-" + parameterTypeName # FIXME: XML escaping required here!
	parameterTypeXML = ET.SubElement(parameterTypesXML, "ParameterType")
	parameterTypeXML.set("Id", parameterTypeId)
	parameterTypeXML.set("Name", parameterTypeName)
	parameterTypeXML.set("Plugin", "")

	#typeRestrictionXML = ET.SubElement(parameterTypeXML, "TypeRestriction")
	#typeRestrictionXML.set("Base", "Value")
	#typeRestrictionXML.set("SizeInBit", "8")

	#enumerationXML = ET.SubElement(typeRestrictionXML, "Enumeration")
	#enumerationXML.set("Id", "")
	#enumerationXML.set("DisplayOrder", "")
	#enumerationXML.set("Text", "")
	#enumerationXML.set("Value", "")

	typeNumberXML = ET.SubElement(parameterTypeXML, "TypeNumber")
	typeNumberXML.set("SizeInBit", "8")
	typeNumberXML.set("Type", "unsignedInt")
	typeNumberXML.set("minInclusive", "0")
	typeNumberXML.set("maxInclusive", "100")
	typeNumberXML.set("SizeInBit", "8")
	# According to spec: UIHint. Missing?

	parameterTypesXML = ET.SubElement(staticXML, "Parameters")

	parameterId = applicationProgramId + "_P-" + "1"
	parameterXML = ET.SubElement(parameterTypesXML, "Parameter")
	parameterXML.set("Id", parameterId)
	parameterXML.set("Name", "Param Name")
	parameterXML.set("ParameterType", parameterTypeId)
	parameterXML.set("Text", "Param Text")
	# According to spec: SuffixText. Missing?
	parameterXML.set("Access", "ReadWrite")
	parameterXML.set("Value", "60")
	# According to spec: Patch Always. Missing?
	# According to spec: Unique Number. Missing?

	#memoryXML = ET.SubElement(parameterXML, "Memory")
	#memoryXML.set("CodeSegment", "")
	#memoryXML.set("Offset", "0")
	#memoryXML.set("BitOffset", "0")

	propertyXML = ET.SubElement(parameterXML, "Property")
	propertyXML.set("ObjectIndex", "0")
	propertyXML.set("PropertyId", "0")
	propertyXML.set("Offset", "0")
	propertyXML.set("BitOffset", "0")

	parameterRefsXML = ET.SubElement(staticXML, "ParameterRefs")

	parameterRefId = parameterId + "_R-1"
	parameterRefXML = ET.SubElement(parameterRefsXML, "ParameterRef")
	parameterRefXML.set("Id", parameterRefId)
	parameterRefXML.set("RefId", parameterId)
	# According to spec: Text. Missing?
	# According to spec: SuffixText. Missing?
	# Obsolete! parameterRefXML.set("DisplayOrder", "1")
	# According to spec: Access. Missing?
	# According to spec: Default Value. Missing?
	parameterRefXML.set("Tag", "1")

	comObjectTableXML = ET.SubElement(staticXML, "ComObjectTable")
	comObjectTableXML.set("CodeSegment", absoluteSegmentId)
	comObjectTableXML.set("Offset", "0")

	comObjectNumber = "0"
	comObjectId = applicationProgramId + "_O-" + comObjectNumber
	comObjectXML = ET.SubElement(comObjectTableXML, "ComObject")
	comObjectXML.set("Id", comObjectId)
	comObjectXML.set("Name", "Allgemein")
	comObjectXML.set("Text", "Allgemein")
	comObjectXML.set("Number", comObjectNumber)
	comObjectXML.set("FunctionText", "Uhrzeit")
	comObjectXML.set("Priority", "Low")
	comObjectXML.set("ObjectSize", "3 Bytes")
	comObjectXML.set("ReadFlag", "Disabled")
	comObjectXML.set("WriteFlag", "Enabled")
	comObjectXML.set("CommunicationFlag", "Enabled")
	comObjectXML.set("TransmitFlag", "Enabled")
	comObjectXML.set("UpdateFlag", "Enabled")
	comObjectXML.set("ReadOnInitFlag", "Disabled")
	comObjectXML.set("DatapointType", "DPST-10-1")
	# Not in spec. Obsolete? comObjectXML.set("VisibleDescription", "")

	comObjectRefsXML = ET.SubElement(staticXML, "ComObjectRefs")

	comObjectRefTag = "1"
	comObjectRefId = comObjectId + "_R-" + comObjectRefTag
	comObjectRefXML = ET.SubElement(comObjectRefsXML, "ComObjectRef")
	comObjectRefXML.set("Id", comObjectRefId)
	comObjectRefXML.set("RefId", comObjectId)
	# According to spec: Name. Missing?
	# According to spec: Text. Missing?
	# According to spec: Function Text. Missing?
	# According to spec: Priority. Missing?
	# According to spec: Object Size. Missing?
	# According to spec: Read Flag. Missing?
	# According to spec: Write Flag. Missing?
	# According to spec: Communication Flag. Missing?
	# According to spec: Transmit Flag. Missing?
	# According to spec: Update Flag. Missing?
	# According to spec: ReadOnInit Flag. Missing?
	#comObjectRefXML.set("DatapointType", "DPST-10-1")
	comObjectRefXML.set("Tag", comObjectRefTag)

	addressTableXML = ET.SubElement(staticXML, "AddressTable")
	addressTableXML.set("CodeSegment", "M-00A6_A-0003-00-0FC5_AS-4000")
	addressTableXML.set("Offset", "0")
	addressTableXML.set("MaxEntries", "200")

	associationTableXML = ET.SubElement(staticXML, "AssociationTable")
	associationTableXML.set("CodeSegment", "M-00A6_A-0003-00-0FC5_AS-4193")
	associationTableXML.set("Offset", "0")
	associationTableXML.set("MaxEntries", "200")

	loadProceduresXML = ET.SubElement(staticXML, "LoadProcedures")
	extensionXML = ET.SubElement(staticXML, "Extension")
	optionsXML = ET.SubElement(staticXML, "Options")

	dynamicXML = ET.SubElement(applicationProgramXML, "Dynamic")

	channelNumber = "0"
	channelId = applicationProgramId + "_CH-" + channelNumber
	channelXML = ET.SubElement(dynamicXML, "Channel")
	channelXML.set("Id", channelId)
	channelXML.set("Name", "Generic")
	channelXML.set("Text", "")
	channelXML.set("Number", channelNumber)

	parameterBlockId = applicationProgramId + "_PB-1"
	parameterBlockXML = ET.SubElement(channelXML, "ParameterBlock")
	parameterBlockXML.set("Id", parameterBlockId)
	parameterBlockXML.set("Name", "General")
	parameterBlockXML.set("Text", "General Settings")
	# According to spec: Access. Missing?
	# According to spec: Help Topic ID. Missing?

	parameterRefRefXML = ET.SubElement(parameterBlockXML, "ParameterRefRef")
	parameterRefRefXML.set("RefId", parameterRefId)

	chooseXML = ET.SubElement(parameterBlockXML, "choose")
	chooseXML.set("ParamRefId", parameterRefId)

	whenXML = ET.SubElement(chooseXML, "when")
	whenXML.set("test", "1")

	comObjectRefRefXML = ET.SubElement(whenXML, "ComObjectRefRef")
	comObjectRefRefXML.set("RefId", "<id>")

#		<ParameterRefRef RefId="M-0083_A-00D7-10-E034_P-3_R-3" />
#		<choose ParamRefId="M-0083_A-00D7-10-E034_P-3_R-3">
#			<when test="1">
#				<ComObjectRefRef RefId="M-0083_A-00D7-10-E034_O-63_R-64" />
 
	return dstRootXML

tree = ET.parse('testdev.xml')
root = tree.getroot()

catalogXML = createCatalog(root)

indent(catalogXML)
#ET.dump(catalogXML)
catalogTree = ET.ElementTree(catalogXML)
catalogTree.write("Catalog.xml", "utf-8", True)

hardwareXML = createHardware(root)

indent(hardwareXML)
ET.dump(hardwareXML)
hardwareTree = ET.ElementTree(hardwareXML)
hardwareTree.write("Hardware.xml", "utf-8", True)

productXML = createProduct(root)

indent(productXML)
#ET.dump(productXML)
productTree = ET.ElementTree(productXML)
productTree.write(applicationProgramId + ".xml", "utf-8", True)

#deviceXML = srcRootXML.find("info")
#deviceName = deviceXML.find("name").text;
