from conans import ConanFile, CMake
import os
import shutil


channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "geotrac")


class LibmosquittoTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libmosquitto/1.5.4-togs1@%s/%s" % (username, channel)
    generators = "txt"

    def build(self):
        if self.settings.arch == "x86" or self.settings.arch == "x86_64":
            source_dir = self.conanfile_directory
            cflags = ""
            if self.settings.arch == "x86":
                cflags += "-m32"
            if self.settings.arch == "x86_64":
                cflags += "-m64"
            ldflags = "-lpthread -lssl -lcrypto"
            os.mkdir("bin")
            lib_path = os.path.join(os.getcwd(), "lib")
            for source_file in os.listdir(self.conanfile_directory):
                full_source_file = os.path.join(source_dir, source_file)
                if(source_file.endswith(".c")):
                    executable = os.path.splitext(source_file)[0]
                    executable_path = os.path.join("bin", executable)
                    self.run("gcc -I. -I../ %s -o %s %s -Llib/ -l%s %s" % (full_source_file, executable_path, cflags, "mosquitto", ldflags))
        else:
            pass

    def imports(self):
        self.copy("*.a", dst="./", src="./lib")
        self.copy("*.h", dst="./", src="./include")

    def test(self):
        if self.settings.arch == "x86" or self.settings.arch == "x86_64":
            os.chdir("bin")
            self.run(".%smosquitto-example" % os.sep)
        else:
            pass
