class Cranecloud < Formula
    include Language::Python::Virtualenv

    desc "CraneCloud CLI tool"
    homepage "https://github.com/crane-cloud/cranecloud-cli"
    url "https://files.pythonhosted.org/packages/source/c/cranecloud/cranecloud-0.0.5.tar.gz"
    sha256 "f7242445a3c9f1452b37f762363d2f23af4c4fc06177595187f12372074b123a"
    license "MIT"

    depends_on "python@3.11"

    resource "Click" do
        url "https://files.pythonhosted.org/packages/source/c/click/click-8.1.8.tar.gz"
        sha256 "ed53c9d8990d83c2a27deae68e4ee337473f6330c040a31d4225c9574d16096a"
    end
      
    resource "requests" do
        url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.32.3.tar.gz"
        sha256 "55365417734eb18255590a9ff9eb97e9e1da868d4ccd6402399eaf68af20a760"
    end
    
    resource "keyring" do
        url "https://files.pythonhosted.org/packages/source/k/keyring/keyring-25.6.0.tar.gz"
        sha256 "0b39998aa941431eb3d9b0d4b2460bc773b9df6fed7621c2dfb291a7e0187a66"
    end
    
    resource "tabulate" do
        url "https://files.pythonhosted.org/packages/source/t/tabulate/tabulate-0.9.0.tar.gz"
        sha256 "0095b12bf5966de529c0feb1fa08671671b3368eec77d7ef7ab114be2c068b3c"
    end
    
    resource "colorama" do
        url "https://files.pythonhosted.org/packages/source/c/colorama/colorama-0.4.6.tar.gz"
        sha256 "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44"
    end
    
    resource "Pygments" do
        url "https://files.pythonhosted.org/packages/source/p/pygments/pygments-2.19.1.tar.gz"
        sha256 "61c16d2a8576dc0649d9f39e089b5f02bcd27fba10d8fb4dcc28173f7a45151f"
    end
    
    resource "rich" do
        url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.9.4.tar.gz"
        sha256 "439594978a49a09530cff7ebc4b5c7103ef57baf48d5ea3184f21d9a2befa098"
    end
    
    resource "python-dotenv" do
        url "https://files.pythonhosted.org/packages/source/p/python-dotenv/python-dotenv-1.0.1.tar.gz"
        sha256 "e324ee90a023d808f1959c46bcbc04446a10ced277783dc6ee09987c37ec10ca"
    end
    
    resource "urllib3" do
        url "https://files.pythonhosted.org/packages/source/u/urllib3/urllib3-2.3.0.tar.gz"
        sha256 "f8c5449b3cf0861679ce7e0503c7b44b5ec981bec0d1d3795a07f1ba96f0204d"
    end
    
    resource "toml" do
        url "https://files.pythonhosted.org/packages/source/t/toml/toml-0.10.2.tar.gz"
        sha256 "b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f"
    end
    
    resource "configparser" do
        url "https://files.pythonhosted.org/packages/source/c/configparser/configparser-7.2.0.tar.gz"
        sha256 "b629cc8ae916e3afbd36d1b3d093f34193d851e11998920fdcfc4552218b7b70"
    end

  
    def install
        # Set environment variable during installation
        ENV["API_BASE_URL"] = "https://api.cranecloud.io"

        virtualenv_install_with_resources
      end
  
    test do
      # Check if the environment variable is set correctly
      assert_match "https://api.cranecloud.io", shell_output("echo $API_BASE_URL")

      system "#{bin}/cranecloud", "--help"
    end
  end
  