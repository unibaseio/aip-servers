import argparse
import asyncio
import datetime
import logging
import os
import random
from typing import Annotated, List

from autogen_core.tools import FunctionTool, Tool

from aip_agent.agents.tool_agent import ToolAgentWrapper

from membase.chain.chain import membase_id

from beeper_server.beeper_chain.beeper import Beeper
from beeper_server.beeper_chain.config import BSC_TESTNET_SETTINGS

wallet_address = os.getenv('MEMBASE_ACCOUNT')
private_key = os.getenv('MEMBASE_PRIVATE_KEY')

beeper_client = Beeper(config=BSC_TESTNET_SETTINGS, admin_wallet_address=wallet_address, admin_private_key=private_key)

from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("mcp-beeper-tool")

@mcp.tool()
async def get_bnb_balance(account_address: str, ctx: Context = None) -> str:
    """get the bnb balance of the account"""
    return beeper_client.get_balance(account_address)
    
@mcp.tool()
async def get_token_balance(account_address: str, token_address: str, ctx: Context = None) -> str:
    """get the token balance of the account"""
    return beeper_client.get_token_balance(account_address, token_address)

@mcp.tool()
async def trade_token(from_token_address: str, to_token_address: str, amount: int, ctx: Context = None) -> str:
    """trade the token from from_token_address to to_token_address with the amount"""
    return beeper_client.make_trade(beeper_client.admin_wallet, beeper_client.admin_private, from_token_address, to_token_address, amount)

@mcp.tool()
async def transfer_bnb(to_account_address: str, amount: int, ctx: Context = None) -> str:
    """transfer the bnb from account to the to_account_address with the amount"""
    return beeper_client.transfer_asset(beeper_client.admin_wallet, beeper_client.admin_private, to_account_address, "", amount)

@mcp.tool()
async def transfer_token(to_account_address: str, token_address: str, amount: int, ctx: Context = None) -> str:
    """transfer the token from account to the token_address with the amount"""
    return beeper_client.transfer_asset(beeper_client.admin_wallet, beeper_client.admin_private, to_account_address, token_address, amount)


async def main(address: str) -> None:
    local_tools: List[Tool] = [
        FunctionTool(
            get_bnb_balance,
            name="get_bnb_balance",
            description="Get the bnb balance of the account",
        ),
        FunctionTool(
            get_token_balance,
            name="get_token_balance",
            description="Get the token balance of the account",
        ),
        FunctionTool(
            trade_token,
            name="trade_token",
            description="Trade the token from from_token_address to to_token_address with the amount",
        ),
        FunctionTool(
            transfer_bnb,
            name="transfer_bnb",
            description="Transfer the bnb from account to the to_account_address with the amount",
        ),
        FunctionTool(
            transfer_token,
            name="transfer_token",
            description="Transfer the token from account to the token_address with the amount",
        ),
    ]

    desc = "This is a beeper agent that can make trade.\n"
    desc += "You can get the bnb balance of the account\n"
    desc += "You can get the token balance of the account\n"
    desc += "You can trade the token from from_token_address to to_token_address with the amount\n"
    desc += "You can transfer the bnb to the to_account_address with the amount\n"
    desc += "you can transfer the token to the to_account_address with the amount\n"
    
    tool_agent = ToolAgentWrapper(
        name=os.getenv("MEMBASE_ID"),
        tools=local_tools,
        host_address=address,
        description=desc
    )
    await tool_agent.initialize()
    print(f"GRPC beeper tool launched as {membase_id} at {address}")
    await tool_agent.stop_when_signal()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an aip grpc tool.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    parser.add_argument("--address", type=str, help="Address to connect to", default="13.212.116.103:8081")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger("autogen_core").setLevel(logging.DEBUG)
        file_name = "agent_" + membase_id + ".log"
        handler = logging.FileHandler(file_name)
        logging.getLogger("autogen_core").addHandler(handler)

    asyncio.run(main(args.address))
