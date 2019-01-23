npsp_lex_locators={
    'breadcrumb': "//li[contains(@class, 'slds-breadcrumb__item')]/span[text()='{}']",
    'mailing_address': "//*[contains(@placeholder,'{}')]",
    'app_launcher':{
        'select-option':'//span/mark[text()="{}"]',
    },
    'object_dd':'//h1[contains(@class,"slds-page-header__title")]//a',
    "record": {
        'button': "//div[@class='actionsContainer']/button[@title='{}']",
        'datepicker':"//div[contains(@class,'uiDatePickerGrid')]/table[@class='calGrid']//span[text()='{}']",
        'month_pick':"//div[@class='dateBar']//a[@title='{}']",
        'edit_form': 'css: div.forcePageBlockItemEdit',
        'list':"//div[contains(@class,'forcePageBlockSectionRow')]/div[contains(@class,'forcePageBlockItem')]/div[contains(@class,'slds-hint-parent')]/div[@class='slds-form-element__control']/div[.//span[text()='{}']][//div[contains(@class,'uiMenu')]//a[@class='select']]",
        'dropdown':"//div[@class='select-options']/ul[@class='scrollable']/li[@class='uiMenuItem uiRadioMenuItem']/a[contains(text(),'{}')]",
        'related': {
            'button': "//article[contains(@class, 'forceRelatedListCardDesktop')][.//img][.//span[@title='{}']]//a[@title='{}']",
            'check_occurrence':'//h2/a/span[@title="{}"]/following-sibling::span',
            'drop-down':'//div[contains(@class, "slds-card")]/header[.//span[@title="{}"]]/parent::*/div/div/div/a[contains(@class, "slds-button")]',
            'title':'//div[contains(@class, "slds-card")]/header[.//span[@title="{}"]]',
            'viewall':'//a[.//span[text()="View All"]/span[text()="{}"]]',
            'item':"//article[contains(@class, 'forceRelatedListCardDesktop')][.//img][.//span[@title='{}']]//h3//a",
            'field_value': '//a[text()="{}"]/ancestor::li//div[contains(@class, "slds-item--detail")]//*[text()="{}"]',
         },
    },
    'popup': "//div[contains(@class, 'uiPopupTarget')][contains(@class, 'visible')]",
    'test':'/html/body/div[6]/table/tbody/tr[23]/td[1]/a',
    'frame':'//iframe[@title= "{}"]',
    'id':'//*[contains(@id,"{}")]',
    'button':'//input[contains(@value,"{}")]',
    'link-text':'//a[text()="{}"]',
    'link-title':'//a[@title="{}"]',
    'checkbox':'//div[contains(@class,"uiInputCheckbox")]/label/span[text()="{}"]/../following-sibling::input[@type="checkbox"]',
    'table_checkbox':'//tbody/tr[./td[2]/a[text()="{}"]]/td/input[@type="checkbox"]',
    'tab': "//div[@class='uiTabBar']/ul[@class='tabs__nav']/li[contains(@class,'uiTabItem')]/a[@class='tabHeader']/span[contains(text(), '{}')]",
    'desktop_rendered': 'css: div.desktop.container.oneOne.oneAppLayoutHost[data-aura-rendered-by]',
    'loading_box': 'css: div.auraLoadingBox.oneLoadingBox',
    'spinner': 'css: div.slds-spinner',
    'modal_field':"//div[contains(@class, 'lookupInput')][./label[contains(text(), '{}')]]/div//span[@class='lookupInput']/input",
    'name':'//tbody/tr/th/span/a',
    'select_name':'//tbody//a[text()= "{}"]',
    'locate_dropdown':'//tbody/tr[{}]/td/span//div/a/lightning-icon',
    'locating_delete_dropdown':'//tbody//a[text()= "{}"]/../../following-sibling::td/span//div/a/lightning-icon',
    'related_name':'//tbody/tr/td/a[contains(@class,"forceOutputLookup")]',
    'rel_loc_dd':'//tbody/tr[{}]/td[4]//lightning-primitive-icon',
    'delete_icon':'//span[contains(text() ,"{}")]/following::span[. = "{}"]/following-sibling::a/child::span[@class = "deleteIcon"]',
    'aff_list':'//div[@role="tablist"]/following::div[@class = "container forceRelatedListSingleContainer"][7]/article/div[@class="slds-card__body"]/div/div/div/div/div/div/div/table/tbody/tr/td[1]',
    'aff_status':'//table[contains(@class,"forceRecordLayout")]/tbody/tr[.//th/div/a[contains(@class,"textUnderline")]][.//td/a[@title="{}"]]/td[3]',
    'aff_id':'//table[contains(@class,"forceRecordLayout")]/tbody/tr[.//th/div/a[contains(@class,"textUnderline")]][.//td/a[@title="{}"]]/th//a',
    'click_aff_id':'//table[contains(@class,"forceRecordLayout")]/tbody/tr/th/div/a[text()="{}"]',
    'check_status':'//div[contains(@class, "forcePageBlockItem")][.//span[text()="{}"]]//following-sibling::div[.//span[contains(@class, "test-id__field-value")]]/span',
    'check_field':'//div[contains(@class, "forcePageBlockItem")][.//span[text()="{}"]]//following-sibling::div[.//span[contains(@class, "test-id__field-value")]]/span/div//a',
    'account_list':'//tbody/tr/th[.//span[contains(@class, "slds-grid")]]/descendant::a[text()="{}"]',
    'dd_options':'//*[@id="p3"]/option[text()="{}"]',
    'related_list_items':'//div[@class = "forceRelatedListContainer"][.//a[contains(@class, "slds-card")]]//span[text() = "{}"]/ancestor::div[contains(@class, "slds-card")]/following-sibling::div[contains(@class, "slds-card")][.//div[contains(@class, "outputLookupContainer")]]//a[text()="{}"]',
    'span_button':'//span[text()="{}"]',
    'header_field_value':'//li[contains(@class, "slds-page-header__detail")][.//span[contains(@class, "slds-form-element__label")][@title="{}"]]//*[text()="{}"]',
    'header_datepicker':'//li[contains(@class, "slds-page-header__detail")][.//p[contains(@class, "slds-text-heading--label")][@title="{}"]]//*[@class="uiOutputDate"]',
    'select_one_record':"//tbody/tr[1]/th/span/a",
    'click_search':'//div[@class="slds-form-element"][./label[text()="{}"]]/div/span/span/input[contains(@id,"inputX")]',
    'field': "//div[contains(@class, 'uiInput')][.//label[contains(@class, 'uiLabel')][.//span[text()='{}']]]//input",
    'field_lookup_value': "//a[@role='option'][.//div[@title='{}']]",
    'header':'//h1[contains(@title,"{}")]',
    'check_related_list_item':'//div[@class = "forceRelatedListContainer"][.//a[contains(@class, "slds-card")]]//span[text() = "{}"]/ancestor::div[contains(@class, "slds-card")]/following-sibling::div[contains(@class, "slds-card")]//tbody//th//a[text()="{}"]',
    'detail_page': {
        'section_header':'//h3//span[text()="{}"]',
        'address':'//h3[contains(@class, "slds-section__title")][.//span[contains(text(),"Address")]]/../..//div[contains(@class, "test-id")]/span[text()= "{}"]/../following-sibling::div//a/div[contains(@class, "slds")]',
        'field':'//h3[contains(@class, "slds-section__title")][.//span[text()="{}"]]/../..//div[contains(@class, "test-id")]/span[text()= "{}"]/../following-sibling::div//span[text()="{}"]',
        'verify_field_value':'//div[contains(@class, "forcePageBlockItem")]/div/div//span[text()="{}"]/../../div[2]/span/span[text() = "{}"]',
    },
    
    'manage_hh_page':{
        'address_link':'//h4[text()="{}"]',
        'address':'//div[contains(@class, "uiInput")][.//label[contains(@class, "uiLabel")]/span[text()="{}"]]/',
        'mhh_checkbox':'//*[@id="SortCanvas"]/li//a[text()="{}"]/ancestor::div[contains(@class, "slds-card__header")]/following-sibling::div[contains(@class,"slds-card__body")]//form//div//label/span[@id = "{}"]',
        'button':'//*[text()="{}"]',
        
    },
    'opportunity':{
        'contact_role':'//div[contains(@class,"listItemBody")][./h3//a[text()="{}"]]//parent::h3/following-sibling::ul/li/div[contains(@class,"forceListRecordItem")]/div[@title="Role:"]/following-sibling::div/span[text()="{}"]',
    },
    'object':{
        'record':'//tbody//a[text()= "{}"]',
        'button': "css: div.windowViewMode-normal ul.forceActionsContainer.oneActionsRibbon a[title='{}']",
        'radio_button':"//div[contains(@class,'changeRecordTypeRightColumn')]/div/label[@class='slds-radio']/div[.//span[text()='{}']]/preceding::div[1]/span[@class='slds-radio--faux']",
        
    },
    'engagement_plan':{
        'input_box':'//fieldset[./legend[text()="{}"]]/div[@class="slds-grid"]//div[@class="requiredInput"]/input',
        'dropdown':'//div[contains(@class,"slds-p-top_small")]/label[text()="{}"]/following-sibling::div/select',
        'checkbox':'//div[contains(@class,"slds-p-top_small")]/label[@class="slds-checkbox"][./span/following-sibling::{}[text()="{}"]/]',
        'button':'//div[contains(@class,"slds-button-group")][.//span[text()="toTask {}"]]/button[contains(text(),"{}")]',
        'check_eng_plan':'//h2/a/span[@title="{}"]//ancestor::div[@class = "slds-card__header slds-grid"]/following-sibling::div//tbody/tr/th/div/a',
        'dd':'//h2/a/span[@title="{}"]//ancestor::div[@class = "slds-card__header slds-grid"]/following-sibling::div//tbody/tr/th/div/a/ancestor::th/following-sibling::td//lightning-primitive-icon',
        'tasks':'//div[@class="slds-section__content"]/ul/li//a[text()="{}"]',
    },
    'levels':{
        'id':'//input[contains(@id,"{}")]',
        'select':'//select[contains(@id,"{}")]',
        
    },
    'payments':{
        'date_loc':"//*[@id='pmtTable']/tbody/tr/td[3]/div//input",       
        'no_payments':'//tbody/tr/td[3]',
        'pay_amount':'//tbody/tr[{}]/td[3]/span/span[text()="{}"]',
        'check_occurrence':'//h2/a/span[@title="{}"]/following-sibling::span',
        'text':'//*[@id="j_id0:vfForm:j_id76:util_formfield:inputx:util_inputfield:inputX"]',
        },
    'gaus':{
        'input_field':'//div[@class="slds-form-element"][./label[text()="{}"]]/div/input',
        },
    'npsp_settings':{
        'panel_sub_link':'//ul/li/a[text()="{}"]',
        'field_value':"//div[@class='slds-form-element'][./label[contains(text(),'{}')]]/div/span",
        'side_panel':"//ul/div[contains(@id,'RecDonations')]/button[1]",
        'list':"//div[contains(@class,'slds-form_horizontal')]/div[@class='slds-form-element']/label[text()='{}']/following-sibling::div/select",
        'multi_list':'//div[contains(@class,"slds-form_horizontal")]/div[@class="slds-form-element"][./label[text()="{}"]]/div//select',
        'list_val':'//div[@class="slds-form-element"][./label[text()="{}"]]/div/span[text()="{}"]',
        'status':'//div[contains(@class,"slds-tile__title")][.//span[text()="{}"]]/div[contains(@class,"slds-col")]//span[text()="{}"]',
        'button':'//form[.//h1[contains(text(),"{}")]]//input[contains(@value,"{}")]',
        'completed':'//span[contains(@class, \'slds-theme_success\')]',
        },
    'data_imports':{
        'status':'//div[contains(@class,"slds-tile__title")][./p[text()="BDI_DataImport_BATCH"]]/div[contains(@class,"slds-col")]/span[text()="{}"]',
        },
    'object_manager':{
        'button':'//input[@title="{}"]'
        }
}
    

extra_locators={
    'related_list_items1':'//div[@class = "forceRelatedListContainer"][.//a[contains(@class, "slds-card")]]//span[text() = "Relationships"]/ancestor::div[contains(@class, "slds-card")]/following-sibling::div[contains(@class, "slds-card")]//tbody//td/span[text()="{}"]',
}
dnd={ ""
    }