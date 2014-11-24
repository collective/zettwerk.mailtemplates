from DateTime import DateTime
from zope.interface import implements
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

from zettwerk.mailtemplates.interfaces import IMessageTemplateContentProvider
from zettwerk.mailtemplates import mailtemplatesMessageFactory as _


class PasswordResetContentProvider(object):

    implements(IMessageTemplateContentProvider)

    def getDescription(self):
        site = getSite()
        return site.translate(
            _(u'Password Reset Link (Variables: password_reset_link and '
              u'expiry_date)'))

    def getContentForMember(self, member):
        site = getSite()
        rtool = getToolByName(site, 'portal_password_reset')
        reset = rtool.requestReset(member.getId())
        return {
            'password_reset_link': rtool.pwreset_constructURL(
                reset['randomstring']),
            'expires_string': site.toLocalizedTime(reset['expires'],
                                                   long_format=1)
        }

    def getPreviewContent(self, member):
        site = getSite()
        return {
            'password_reset_link': site.absolute_url(),
            'expires_string': site.toLocalizedTime(DateTime(),
                                                   long_format=1)
        }
