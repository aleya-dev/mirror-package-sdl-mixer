from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import rmdir, rm, collect_libs
import os


required_conan_version = ">=2.0"


class OggConan(ConanFile):
    name = "sdl-mixer"
    version = "ace2d37"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaConanBase"
    ignore_cpp_standard = True

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    requires = ["sdl/3.1.2@aleya/public", "vorbis/1.3.7@aleya/public"]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["SDL3MIXER_VENDORED"] = False
        tc.variables["SDL3MIXER_INSTALL_MAN"] = False
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "SDL3_mixer")
        self.cpp_info.set_property("cmake_target_name", "SDL3_mixer::SDL3_mixer")
        self.cpp_info.set_property("pkg_config_name", "SDL3_mixer")

        self.cpp_info.libs = collect_libs(self)
