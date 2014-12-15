let
region = "eu-west-1";
zone = "eu-west-1a";

ec2-builder = { resources, pkgs, lib, ... }: let
  tompkgs = import <tompkgs> {};
  in {
  deployment.targetEnv = "ec2";
  deployment.ec2.region = region;
  deployment.ec2.zone = zone;
  deployment.ec2.instanceType = "m3.medium";
  deployment.ec2.keyPair = resources.ec2KeyPairs.keys;
  deployment.ec2.spotInstancePrice = 2;
  deployment.ec2.securityGroups = [ resources.ec2SecurityGroups.http-ssh ];

  networking.firewall.enable = true;
  networking.firewall.allowedTCPPorts = [ 22 80 443 ];
  networking.firewall.allowPing = true;

  services.openssh.enable = true;
  nix.distributedBuilds = true;
  
  # We know from the metadata dump that the totality of pypi is
  # 123GiB. We also need a reasonably large working area so we
  # allocate that as well.
  deployment.ec2.ebsInitialRootDiskSize = 200;

  environment.systemPackages = [
    pkgs.git tompkgs.fullpypi
  ];
};

in {
  network.description = "fullpypi";

  # Exactly one machine:
  builder = ec2-builder;

  resources.ec2KeyPairs.keys = { inherit region; };
  resources.ec2SecurityGroups.http-ssh = {
    inherit region;
    rules = [
      { fromPort = 22; toPort = 22; sourceIp = "0.0.0.0/0"; }
      { fromPort = 80; toPort = 80; sourceIp = "0.0.0.0/0"; }
      { fromPort = 443; toPort = 443; sourceIp = "0.0.0.0/0"; }
    ];
  } ;
}
