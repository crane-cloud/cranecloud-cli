class Cranecloud < Formula
    include Language::Python::Virtualenv

    desc "CraneCloud CLI tool"
    homepage "https://github.com/crane-cloud/cranecloud-cli"
    url "https://files.pythonhosted.org/packages/source/c/cranecloud/cranecloud-0.0.5.tar.gz"
    sha256 "f7242445a3c9f1452b37f762363d2f23af4c4fc06177595187f12372074b123a"
    license "MIT"

    depends_on "python@3.11"
  
    def install
        virtualenv_install_with_resources
        
        # Get the path to the original script
        original_script = bin/"cranecloud"
        original_content = File.read(original_script)
        
        # Create a new script with the environment variable
        File.write(original_script, <<~EOS)
          #!/bin/bash
          export API_BASE_URL="https://api.cranecloud.io"
          exec /usr/bin/env python3 "#{libexec}/bin/cranecloud" "$@"
        EOS
        
        chmod 0755, original_script
      end
  
    test do
      system "#{bin}/cranecloud", "--help"
    end
  end
  