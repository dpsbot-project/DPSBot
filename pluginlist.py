
import os
import sys


class Pluginlist():
       def __init__(self):
              sys.path.append(os.getcwd())
              self.plugin_path =os.path.dirname(os.path.realpath(__file__)) + "/plugin/"
              self.refresh()

       def searcher(self, dir: str):
              return os.listdir(self.plugin_path + dir)

       def refresh(self):
              self.default = self.searcher("default")
              self.non_default = self.searcher("non-default")
              self.half_abandoned = self.searcher("half-abandoned")

       def move(self, module_name: str, original_dir: str, new_dir: str):
              if not ".." in original_dir and not ".." in new_dir:
                     try:
                            os.rename(self.plugin_path + original_dir + "/" + module_name + ".py",
                                   self.plugin_path + new_dir + "/" + module_name + ".py")
                            self.refresh()
                            return True
                     except:
                            return _("잘못된 접근입니다.")
              else:
                     return _("상위 디렉토리 접근은 불가합니다.")

       def get(self):
              return {"default":self.default, "non-default":self.non_default, "half-abondoned":self.half_abandoned}
pluginlist= Pluginlist()
