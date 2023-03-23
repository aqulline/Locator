from jnius import autoclass
from jnius import cast


# "android.permission.CALL_PHONE"

def call(num):
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    intent = Intent(Intent.ACTION_CALL)
    intent.setData(Uri.parse("tel:" + num))
    currentActivity = cast('android.app.Activity',
                           PythonActivity.mActivity)
    currentActivity.startActivity(intent)
