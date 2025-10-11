#!/usr/bin/env python3
import os

import aws_cdk as cdk
from cdk.stack.node2 import Node2Ec2Instance

from utils.utils import load_value_frm_config

app = cdk.App()
Node2Ec2Instance(app, "Node3Kubedm",env=cdk.Environment(account=load_value_frm_config("ACCOUNT"), region=load_value_frm_config("REGION")))

app.synth()
