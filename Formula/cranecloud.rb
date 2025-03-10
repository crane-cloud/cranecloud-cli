class Cranecloud < Formula
    desc "CraneCloud CLI tool"
    homepage "https://github.com/crane-cloud/cranecloud-cli"
    url "https://files.pythonhosted.org/packages/source/c/cranecloud/cranecloud-0.0.5.tar.gz"
    sha256 "f7242445a3c9f1452b37f762363d2f23af4c4fc06177595187f12372074b123a"
    license "MIT"

    depends_on "python@3.8"
  
    def install
        virtualenv_install_with_resources
        (bin/"cranecloud").write_env_script libexec/"bin/cranecloud", API_BASE_URL: "https://api.cranecloud.io"
    end
  
    test do
      system "#{bin}/cranecloud", "--help"
    end
  end
  