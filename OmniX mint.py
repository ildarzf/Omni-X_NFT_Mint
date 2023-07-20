import json
from web3.auto import Web3
import decimal
import random
import time
from tqdm import tqdm
from loguru import logger


############################################  ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ  #######################################
wal_sleep_min = 110    # минимальная задержка между кошелька
wal_sleep_max = 250    # максимальная задержка между кошелька
time_to_conf = 360 #  Время ожидания подтверждения транзакции в секундках (уменьшить до 120 когда перестанет лагать BSC)
Gwei = 50  # если газ выше уходим в ожидание
rpc_op = "https://mainnet.optimism.io"   # Нода Майннет Басе
rpc_eth = "https://1rpc.io/eth"    # Нода Эфира
shuffle = True # False / True Перемешивать кошельки или нет

nft_nummin = 10    # min минт нфт
nft_nummax = 20    # max минт нфт
###########################################################################################################


def intToDecimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"] * decimal)))

def sleep_indicator(sec):
    for i in tqdm(range(sec), desc='Пауза', bar_format="{desc}: {n_fmt}c /{total_fmt}c {bar}", colour='green'):
        time.sleep(1)

def mintnft(private_key):
    web3 = Web3(Web3.HTTPProvider(rpc_op))
    mint_abi ='[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_lzEndpoint","type":"address"},{"internalType":"uint256","name":"_startId","type":"uint256"},{"internalType":"uint256","name":"_maxId","type":"uint256"},{"internalType":"uint256","name":"_maxGlobalId","type":"uint256"},{"internalType":"string","name":"_baseTokenURI","type":"string"},{"internalType":"string","name":"_hiddenURI","type":"string"},{"internalType":"uint16","name":"_tax","type":"uint16"},{"internalType":"uint256","name":"_price","type":"uint256"},{"internalType":"address","name":"_taxRecipient","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"OperatorNotAllowed","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"_hashedPayload","type":"bytes32"}],"name":"CreditCleared","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"_hashedPayload","type":"bytes32"},{"indexed":false,"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"CreditStored","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":false,"internalType":"uint64","name":"_nonce","type":"uint64"},{"indexed":false,"internalType":"bytes","name":"_payload","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"_reason","type":"bytes"}],"name":"MessageFailed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":true,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":true,"internalType":"address","name":"_toAddress","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"ReceiveFromChain","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":false,"internalType":"uint64","name":"_nonce","type":"uint64"},{"indexed":false,"internalType":"bytes32","name":"_payloadHash","type":"bytes32"}],"name":"RetryMessageSuccess","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"bytes","name":"_toAddress","type":"bytes"},{"indexed":false,"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"}],"name":"SendToChain","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"_dstChainIdToBatchLimit","type":"uint256"}],"name":"SetDstChainIdToBatchLimit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"_dstChainIdToTransferGas","type":"uint256"}],"name":"SetDstChainIdToTransferGas","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"_type","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"_minDstGas","type":"uint256"}],"name":"SetMinDstGas","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_minGasToTransferAndStore","type":"uint256"}],"name":"SetMinGasToTransferAndStore","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"precrime","type":"address"}],"name":"SetPrecrime","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_path","type":"bytes"}],"name":"SetTrustedRemote","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_remoteAddress","type":"bytes"}],"name":"SetTrustedRemoteAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DEFAULT_PAYLOAD_SIZE_LIMIT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"FUNCTION_TYPE_SEND","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"OPERATOR_FILTER_REGISTRY","outputs":[{"internalType":"contract IOperatorFilterRegistry","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_financeDetails","outputs":[{"internalType":"address payable","name":"beneficiary","type":"address"},{"internalType":"address payable","name":"taxRecipient","type":"address"},{"internalType":"uint16","name":"tax","type":"uint16"},{"internalType":"uint256","name":"price","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"clearCredits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"dstChainIdToBatchLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"dstChainIdToTransferGas","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"},{"internalType":"bool","name":"_useZro","type":"bool"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"estimateSendBatchFee","outputs":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"zroFee","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"bool","name":"_useZro","type":"bool"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"estimateSendFee","outputs":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"zroFee","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint64","name":"","type":"uint64"}],"name":"failedMessages","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"forceResumeReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"_configType","type":"uint256"}],"name":"getConfig","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"}],"name":"getTrustedRemoteAddress","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"isTrustedRemote","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lzEndpoint","outputs":[{"internalType":"contract ILayerZeroEndpoint","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"lzReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"maxGlobalId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxTokensPerMint","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"metadata","outputs":[{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"hiddenMetadataURI","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"uint16","name":"","type":"uint16"}],"name":"minDstGasLookup","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minGasToTransferAndStore","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nbTokens","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"nonblockingLzReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"payloadSizeLimitLookup","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"precrime","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"retryMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256[]","name":"_tokenIds","type":"uint256[]"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"address","name":"_zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"sendBatchFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"address","name":"_zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"sendFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"uint256","name":"_configType","type":"uint256"},{"internalType":"bytes","name":"_config","type":"bytes"}],"name":"setConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstChainIdToBatchLimit","type":"uint256"}],"name":"setDstChainIdToBatchLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_dstChainIdToTransferGas","type":"uint256"}],"name":"setDstChainIdToTransferGas","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address payable","name":"beneficiary","type":"address"},{"internalType":"address payable","name":"taxRecipient","type":"address"},{"internalType":"uint16","name":"tax","type":"uint16"},{"internalType":"uint256","name":"price","type":"uint256"}],"internalType":"struct AdvancedONFT721ATimed.FinanceDetails","name":"_finance","type":"tuple"}],"name":"setFinanceDetails","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64","name":"_maxTokensPerMint","type":"uint64"}],"name":"setMaxTokensPerMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"hiddenMetadataURI","type":"string"}],"internalType":"struct AdvancedONFT721ATimed.Metadata","name":"_metadata","type":"tuple"}],"name":"setMetadata","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint16","name":"_packetType","type":"uint16"},{"internalType":"uint256","name":"_minGas","type":"uint256"}],"name":"setMinDstGas","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_minGasToTransferAndStore","type":"uint256"}],"name":"setMinGasToTransferAndStore","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"_start","type":"uint32"},{"internalType":"uint32","name":"_end","type":"uint32"}],"name":"setMintRange","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"bool","name":"saleStarted","type":"bool"},{"internalType":"bool","name":"revealed","type":"bool"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"mintLength","type":"uint256"}],"internalType":"struct AdvancedONFT721ATimed.NFTState","name":"_state","type":"tuple"}],"name":"setNftState","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_size","type":"uint256"}],"name":"setPayloadSizeLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_precrime","type":"address"}],"name":"setPrecrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setReceiveVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setSendVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_path","type":"bytes"}],"name":"setTrustedRemote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"internalType":"bytes","name":"_remoteAddress","type":"bytes"}],"name":"setTrustedRemoteAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"state","outputs":[{"internalType":"bool","name":"saleStarted","type":"bool"},{"internalType":"bool","name":"revealed","type":"bool"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"mintLength","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"storedCredits","outputs":[{"internalType":"uint16","name":"srcChainId","type":"uint16"},{"internalType":"address","name":"toAddress","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"bool","name":"creditsRemain","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"trustedRemoteLookup","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    minter = web3.to_checksum_address('0xD12999440402d30F69E282d45081999412013844') # контракт omni-X mint NFT
    minting = web3.eth.contract(address=minter, abi=mint_abi)
    address = web3.eth.account.from_key(private_key).address
    gasLimit = random.randint(130000,160000)
    _nbTokens = random.randint(nft_nummin, nft_nummax)
    try:
        tx = minting.functions.mint(_nbTokens
        ).build_transaction({
          'from': address,
          'gas': gasLimit,
          'gasPrice':  web3.eth.gas_price,
          'nonce': web3.eth.get_transaction_count(address)
          })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        logger.info(f'Mint NFT: Transaction hash: https://optimistic.etherscan.io/tx/{tx_hash.hex()}')
        logger.info('Жду подтверждение...')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=time_to_conf)
        logger.success('Отправил')
    except Exception as err:
        logger.error(f'  Ошибка.   {err}')
def minter():
    with open('wallets.txt', 'r') as f:
        wallets = f.read().splitlines()
    if shuffle:
        random.shuffle(wallets)
    num = 0
    for wallet in wallets:
        try:
            num= num+1
            web3 = Web3(Web3.HTTPProvider(rpc_op))
            account = web3.eth.account.from_key(wallet).address
            logger.info(f'№ {num} - {account}')
            while True:
                web3 = Web3(Web3.HTTPProvider(rpc_eth))
                current_gas_price = web3.eth.gas_price
                current_gas_price_gwei = web3.from_wei(current_gas_price, 'gwei')
                if round(current_gas_price_gwei, 1) <= Gwei:
                   mintnft(wallet)
                   break
                else:
                   logger.info(f'GWEI {round(current_gas_price_gwei, 1)}  Ждем Gwei ниже {Gwei}')
                   sleep_indicator(30)
            time_wait_wal = random.randint(wal_sleep_min, wal_sleep_max)
            sleep_indicator(time_wait_wal)
        except Exception as err:
            logger.error(f'  Ошибка.   {err}')


if __name__ == '__main__':
        minter()



