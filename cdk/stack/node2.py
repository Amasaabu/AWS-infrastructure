from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    # aws_sqs as sqs,
)
from constructs import Construct

from cdk.constructs.ec2_construct import Ec2InstanceConstruct

from utils.utils import *
class Node2Ec2Instance(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        



        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=load_value_frm_config("VPC_ID"))

        subnet = ec2.Subnet.from_subnet_attributes(self, "pub_Subnet", subnet_id=load_value_frm_config("SUBNET_ID"), availability_zone="us-east-1d")
        subnet_selection = ec2.SubnetSelection(subnets=[subnet])

        worker_kubedm_sg= ec2.SecurityGroup.from_security_group_id(self, "kubed_sg", security_group_id=load_value_frm_config("SECURITY_GROUP_ID"))
        

        Ec2InstanceConstruct(self, "Node3", vpc, worker_kubedm_sg, "Node2-kubedm", load_value_frm_config("KEY_PAIR_ID"), load_value_frm_config("KEY_PAIR_NAME"), subnet=subnet_selection, abs_path_to_user_data="utils/setup.sh" )
    
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
