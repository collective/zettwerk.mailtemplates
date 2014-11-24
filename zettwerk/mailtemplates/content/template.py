"""Definition of the Template content type
"""

from zope.interface import implements
from zope.component import getUtilitiesFor, getUtility

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from zettwerk.mailtemplates import mailtemplatesMessageFactory as _

from zettwerk.mailtemplates.interfaces import (
    ITemplate,
    IMessageTemplateContentProvider
)
from zettwerk.mailtemplates.config import PROJECTNAME

from Products.CMFCore.utils import getToolByName


TemplateSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'templateId',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Template id"),
            description=_(u"a unique id for the template. You can use a "
                          u" custom one or use one of the defaults: "
                          u"'registration', 'password_reset'"),
        ),
        required=True,
    ),

    atapi.LinesField(
        'contentProviders',
        storage=atapi.AnnotationStorage(),
        vocabulary='listContentProviders',
        enforceVocabulary=True,
        widget=atapi.MultiSelectionWidget(
            label=_(u'Content Providers'),
            description=_(
                u'Content Providers provide one or more variables to insert '
                u'content into messages. This content can differ for each '
                u'recipient. After selecting one or more content providers '
                u'for a template you can use the variables they provide in '
                u'the template.')
        )
    )


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TemplateSchema['title'].storage = atapi.AnnotationStorage()
TemplateSchema['title'].widget.label = _(u'Subject')
TemplateSchema['title'].widget.description = _(u'Enter the mail subject')

TemplateSchema['description'].storage = atapi.AnnotationStorage()
TemplateSchema['description'].widget.label = _(u'Mail body text')
TemplateSchema['description'].widget.description = _(
    u'You can use python string substitution syntax to insert dynamic '
    u'values. Supported variables are: username, fullname, portal_url, '
    u'portal_name, and additional variables provided by enabled content '
    u'providers. Example: "Hello %(fullname)s"'
)


schemata.finalizeATCTSchema(TemplateSchema, moveDiscussion=False)


class Template(base.ATCTContent):
    """Description of the Example Type"""
    implements(ITemplate)

    meta_type = "Template"
    schema = TemplateSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    templateId = atapi.ATFieldProperty('templateId')

    def getSubject(self):
        """ return the title """
        return self.Title()

    def getBody(self):
        """ return the description """
        return self.Description()

    def listContentProviders(self):
        providers = getUtilitiesFor(IMessageTemplateContentProvider)
        return [(name, utility.getDescription()) for
                name, utility in providers if name]

    def getRenderedBody(self, member, preview=False):
        """ will fail on invalid substitutions
        returns empty strings if the member does not
        have the information or is empty
        """
        ptool = getToolByName(self, 'portal_url')

        portal_url = ptool()
        portal_name = ptool.getProperty('title', '')
        username = member.getId()
        fullname = member.getProperty('fullname', '')

        data = {'username': username,
                'fullname': fullname,
                'portal_url': portal_url,
                'portal_name': portal_name}

        body = self.getBody()

        for content_provider in self.getContentProviders():
            utility = getUtility(IMessageTemplateContentProvider,
                                 name=content_provider)
            if preview:
                data.update(utility.getPreviewContent(member))
            else:
                data.update(utility.getContentForMember(member))

        return body % data

    def getRenderedBodyPreview(self):
        """ return the rendered mail text, will not fail on errors,
        and decoded for gui """
        mtool = getToolByName(self, 'portal_membership')
        ptool = getToolByName(self, 'portal_properties')
        output_enc = ptool.site_properties.getProperty('default_charset')

        try:
            body = self.getRenderedBody(mtool.getAuthenticatedMember(),
                                        preview=True)
            if output_enc != 'utf-8':
                return body.encode(output_enc)
            else:
                return body
        except Exception as reason:
            return 'ERROR: %s' % (repr(reason))

atapi.registerType(Template, PROJECTNAME)
