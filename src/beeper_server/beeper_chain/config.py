from dotenv import load_dotenv
import os
load_dotenv()

# BSC / BSC_TESTNET
CHAIN = os.getenv('CHAIN', 'BSC_TESTNET')
CHAIN_ID = int(os.getenv('CHAIN_ID', '97'))
BSC_TESTNET_SETTINGS = {
    "RPC": "https://bsc-testnet-rpc.publicnode.com",
    "Explorer": "https://testnet.bscscan.com/",
    "ChainId": 97,
    "PancakeV3Factory": "0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865",
    "PancakeV3SwapRouter": "0x1b81D678ffb9C0263b24A97847620C99d213eB14",
    "PancakeV3PoolDeployer": "0x41ff9AA7e16B8B1a8a8dc4f0eFacd93D02d071c9",
    "PostionManage": "0x427bF5b37357632377eCbEC9de3626C71A5396c1",
    "Beeper": "0x6257761AB5a92E89cD727Ea6650E1188D738007a",
    "BeeperUtil": "0xa29Bfb0ab2EED7299659B4AAB69a38a77Fd62aa5",
}

BSC_MAINNET_SETTINGS = {
    "RPC": "https://bsc-rpc.publicnode.com",
    "Explorer": "https://www.bscscan.com/",
    "ChainId": 56,
    "PancakeV3Factory": "0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865",
    "PancakeV3SwapRouter": "0x1b81D678ffb9C0263b24A97847620C99d213eB14",
    "PancakeV3PoolDeployer": "0x41ff9AA7e16B8B1a8a8dc4f0eFacd93D02d071c9",
    "PostionManage": "0x46A15B0b27311cedF172AB29E4f4766fbE7F4364",
    "Beeper": "0x488FF32dABC2cC42FEc96AED5F002603bB3CEd3F",
    "BeeperUtil": "0x5c84c3c6dF5A820D5233743b4Eea5D32bEa30362",
}

CHAIN_SETTINGS = {
    'BSC': BSC_MAINNET_SETTINGS,
    'BSC_TESTNET': BSC_TESTNET_SETTINGS,
}

DB_SETTINGS = {
    "dbname": os.getenv('DB_NAME', "unibase_test"),
    "user": os.getenv('DB_USER', "unibase"),
    "password": os.getenv('DB_PASSWORD', "S5OOsJHdMZke5hDz4a0foTtsiduRh0E"),
    "host": os.getenv('DB_HOST', "unibase-instance-1.cr0swyc6wyh6.ap-southeast-1.rds.amazonaws.com"),
    "port": os.getenv('DB_PORT', 5432),
}

admin_wallet_address = os.getenv('ADMIN_ADDRESS')
admin_private_key = os.getenv('ADMIN_PRIVATE_KEY')
PRIVY_APP_ID = os.getenv('PRIVY_APP_ID')
PRIVY_APP_SECRET = os.getenv('PRIVY_APP_SECRET')