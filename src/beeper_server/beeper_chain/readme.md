# beeper

## example

see ../chain_test.py

## privy intergation

for test:
privy_app_id:cm5lt8cxs022d4bbclcvh1kn8
PRIVY_APP_SECRET:2oLDPn5x7ANhK2CAxSctoPo4LcKynRqgoDaVsrddXPq2eJRUpMgjVJawvAHEHsZXjvdC8WqRZsoT1FM4pvr6qFKv

set privay_app_id when create beeper instance:

+ create_wallet() -> wallet_address, wallet_id
wallet_address eth address, wallet_id is used to interact with privy, saved in DB
+ use wallet_id instead of private_key when call function, for example: transfer(wallet_address, wallet_id, to_address, amount)

## function

### deploy

deploy by admin, only once

### depoy_token

by admin


### make_trade
by user
token_address is "", means native token(bnb)

币-币购买


### transfer_asset
by user 
token_address is "", means native token(bnb)

转账，本币或代币

### claim_reward
by user

获取流动性奖励，平台得到60%， 用户40%