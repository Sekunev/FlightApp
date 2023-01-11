from rest_framework import permissions


# IsAdminUser --> has_permission'i override yapalım.
# permissions classları boolean değer döner.
# Normal kullanıcılar SAFE_METHODS(GET, HEAD, OPTİONS), staff yani admin kullanıcılar tüm crud işlemlerini yapsın.
class IsStafforReadOnly(permissions.IsAdminUser):

        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True
            
            return bool(request.user and request.user.is_staff) # auth olmuş ve staff ise