# -*- extra stuff goes here -*-
from template import ITemplate
ITemplate

from mailtemplatetool import IMailTemplateTool
IMailTemplateTool


from zope.interface import Interface


class IMessageTemplateUserFilter(Interface):

    def getTitle():
        """ returns a translated human readable name of the filter """

    def filterdMembers(members):
        """ filter the list of members like you want """


class IMessageTemplateUserObjectFilter(Interface):

    def getTitle():
        """ returns a translated human readable name of the filter """

    def filterdMembers(members):
        """ filter the list of members like you want """

    def objectList():
        """ return a list of objects, which might be choosen as extra
        filter criterium. """


class IMessageTemplateContentProvider(Interface):
    """ Content Providers can provide additional variables for use inside
        templates. Content Providers are registered as global utilities. For
        each templates a list of content providers can be enabled: The
        getContentForMember method of these content providers will then be
        called during message generation for each recipient to provide variable
        contents.

    """

    def getDescription():
        """ A translated human readable description of the content
            provider. The description should contain the variables this content
            provider does provide.

        """

    def getContentForMember(member):
        """ Returns a dict mapping one or more variable names to strings which
            will replace the corresponding variables in the message to member.

        """

    def getPreviewContent(member):
        """ A dict mapping one or more variable names to strings which will
            replace the corresponding variables in a preview message. Member is
            always the member displaying the preview message.

        """
