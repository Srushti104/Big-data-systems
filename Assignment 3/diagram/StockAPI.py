# diagram.py
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.programming.flowchart import Database
from diagrams.programming.framework import Fastapi
from diagrams.generic.database import SQL
from diagrams.onprem.auth import Oauth2Proxy
from diagrams.onprem.client import User
from diagrams.saas.analytics import Snowflake
from diagrams.programming.flowchart import Document

with Diagram("Stock API", show=False):

    api= [Fastapi("API")]

    doc = Document("document")

   # with Cluster("auth enabled FastAPI"):
    a = User("customer") >> Oauth2Proxy("auth") >> api

    a >> doc
    a >> Snowflake('Snowflake')






# with Diagram("Clustered Web Services", show=False):
#     dns = Route53("dns")
#     lb = ELB("lb")
#
#     with Cluster("Services"):
#         svc_group = [ECS("web1"),
#                      ECS("web2"),
#                      ECS("web3")]
#
#     with Cluster("DB Cluster"):
#         db_master = RDS("userdb")
#         db_master - [RDS("userdb ro")]
#
#     memcached = ElastiCache("memcached")
#
#     dns >> lb >> svc_group
#     svc_group >> db_master
#     svc_group >> memcached