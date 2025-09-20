import hashlib
import logging
import os
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

# we can make the expiry as a value taken from the
token_expiry_date_in = "project_api.access_token_token_expiry_date_in"


def random_token(length=40, prefix="access_token"):
    # we can agree here how we can manage the token?
    rbytes = os.urandom(length)
    return "{}_{}".format(prefix, str(hashlib.sha1(rbytes).hexdigest()))


class APIAccessToken(models.Model):
    _name = "api.access_token"
    _description = "API Access Token"

    token = fields.Char("Access Token", required=True)
    user_id = fields.Many2one("res.users", string="User", required=True)
    token_expiry_date = fields.Datetime(string="Token Expiry Date", required=True)
    scope = fields.Char(string="Scope")

    def find_or_create_token(self, user_id=None, create=False):
        if not user_id:
            user_id = self.env.user.id

        access_token = self.env["api.access_token"].sudo().search([("user_id", "=", user_id)], order="id DESC", limit=1)
        if access_token:
            access_token = access_token[0]
            if access_token.has_expired():
                access_token = None
        if not access_token and create:
            # token_expiry_date = datetime.now() + timedelta(seconds=int(self.env.ref(token_expiry_date_in).sudo().value))
            token_expiry_date = datetime.now() + timedelta(days=1)
            vals = {
                "user_id": user_id,
                "scope": "userinfo",
                "token_expiry_date": token_expiry_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                "token": random_token(),
            }
            access_token = self.env["api.access_token"].sudo().create(vals)
        if not access_token:
            return None
        return access_token.token

    def is_valid(self, scopes=None):
        """
        Checks if the access token is valid.

        :param scopes: An iterable containing the scopes to check or None
        """
        self.ensure_one()
        return not self.has_expired() and self._allow_scopes(scopes)

    def has_expired(self):
        self.ensure_one()
        return datetime.now() > fields.Datetime.from_string(self.token_expiry_date)

    def _allow_scopes(self, scopes):
        self.ensure_one()
        if not scopes:
            return True

        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)


class Users(models.Model):
    _inherit = "res.users"

    def sum_numbers(self, x, y):
        return x + y

    token_ids = fields.One2many("api.access_token", "user_id", string="Access Tokens")
