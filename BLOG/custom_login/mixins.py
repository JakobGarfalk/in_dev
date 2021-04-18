class UserMixin(object):
    '''
    Jeg customiserer denne; i mixins.py
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    '''

#    if not PY2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    ### is_admin har jeg lagt til for å implentere ulike lag av autorisering
    @property
    def is_admin(self):
        return True if self.rettighet=="admin" else False
        # if self.rettighet=="admin": return True
        # print ("Fra mixins.py, self.rettighet:",self.rettighet)
        # return False
    @is_admin.setter
    def is_admin(self, verdi):
        if verdi==True:
            self.rettighet="admin"
        if verdi==False:
            self.rettighet="bruker"

    #u.is_admin=True
    # class C(object):
    # def __init__(self):
    #     self._x = None

    # @property
    # def x(self):
    #     """I'm the 'x' property."""
    #     return self._x

    # @x.setter
    # def x(self, value):
    #     self._x = value

    # @x.deleter
    # def x(self):
    #     del self._x

    def get_id(self):
        try:
            #return text_type(self.id) # fjerner PY2 compabilitet
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class AnonymousUserMixin(object):
    '''
    This is the default object for representing an anonymous user.
    '''
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True
    
    @property
    def is_admin(self):
        return False

    def get_id(self):
        return
