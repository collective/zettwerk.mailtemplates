

def import_various(context):
    """ setup the thing """
    portal = context.getSite()

    ## remove our tool from the catalog
    if 'portal_mail_templates' in portal:
        portal.portal_mail_templates.unindexObject()
