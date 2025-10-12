from aws_cdk import (
    aws_ec2 as ec2, Tags,
)
from constructs import Construct
import os
from pathlib import Path
# Construct is like the class

class Ec2InstanceConstruct(Construct):
    def __init__(self, scope: Construct, id: str, vpc, security_group, instance_name: str, ssh_key_id: str, ssh_key_pair_name: str, subnet=None, abs_path_to_user_data: str=None, **kwargs):
        super().__init__(scope, id, **kwargs)
        # Create EC2 instance using existing VPC and SG

        ubuntu_version = "noble" 
        self.instance = ec2.Instance(
            self, "Ec2Instance",
            instance_name=instance_name,
            vpc=vpc,
            security_group=security_group,
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.from_ssm_parameter(f"/aws/service/canonical/ubuntu/server/{ubuntu_version}/stable/current/amd64/hvm/ebs-gp2/ami-id", os=ec2.OperatingSystemType.LINUX),
            key_pair=ec2.KeyPair.from_key_pair_name(self, id=ssh_key_id, key_pair_name=ssh_key_pair_name),
            vpc_subnets=subnet,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(30, volume_type=ec2.EbsDeviceVolumeType.GP2, delete_on_termination=True),
            )],
            role=None
        )

        if abs_path_to_user_data!=None:
            BASE_DIR = Path(__file__).parent.parent.parent / abs_path_to_user_data
            try:
                with open(BASE_DIR, "r", encoding="utf-8") as f:
                    self.instance.add_user_data(f.read())
            except Exception as e:
                raise Exception(f"Failed to read user data file {BASE_DIR}: {e}") from e


        # Add user data .sh script from file
        # with open("cdk/scripts/user_data.sh", "r") as f:
        #     user_data_script = f.read()
        # self.instance.add_user_data(user_data_script)

        # Optional: Add tags or user data
        Tags.of(self.instance).add("Name", instance_name)
