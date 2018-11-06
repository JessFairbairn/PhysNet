import os

def _get_static_folder():
#     return os.environ.get('STATIC_DIR', 'static')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        root = dir_path.split('/')
        try:
                index = root.index('PhysNet')
                if index > -1:
                        return '/'.join(root[0:index + 1]) + '/web/static'
        except ValueError:

                pwd = os.path.dirname(os.path.realpath(__file__))
                root = pwd.split('/')
                if root[-1] == 'web':
                        return 'static'
                else:
                        return 'web/static'