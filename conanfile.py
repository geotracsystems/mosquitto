from conans import ConanFile, CMake, tools
import os


class LibmosquittoConan(ConanFile):
    name = "libmosquitto"
    version = "1.4.14"
    license = "EDL/EPL"
    description = "Mosquitto MQTT client library"
    url = "https://github.com/geotracsystems/mosquitto"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = []
    generators = "txt"
    exports_sources = "*"

    def build(self):
        source_dir = 'lib/'
        compiler = os.environ["CC"]
        cflags = "-I. -I{} -DWITH_THREADING".format(source_dir)
        static_lib = "libmosquitto.a"
        if self.settings.arch == "x86":
            cflags += " -m32"
        if self.settings.arch == "x86_64":
            cflags += " -m64"
        object_files = ""
        for source_file in os.listdir(source_dir):
            if(source_file.endswith(".c")):
                full_source_file = os.path.join(source_dir, source_file)
                object_file = os.path.splitext(full_source_file)[0] + '.o'
                object_files += " " + object_file
                self.run('%s %s -c %s -o %s' % (compiler, cflags, full_source_file, object_file))
        self.run('ar cr %s %s' % (os.path.join(source_dir, static_lib), object_files))

    def package(self):
        self.copy("*.a", dst="lib", keep_path=True)
        self.copy("mosquitto.h", dst="include", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["mosquitto"]
