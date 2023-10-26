import streamlit as st
from web3 import Web3


# Initialize Web3
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))  
contract_address = "0x8467364C3e1D318cD9a4150BD8Fb660f3E0307D9"  
contract_abi = """[
	{
		"inputs": [],
		"name": "claimWinnings",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bool",
				"name": "teamAWon",
				"type": "bool"
			}
		],
		"name": "decideOutcome",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bool",
				"name": "forTeamA",
				"type": "bool"
			}
		],
		"name": "placeBet",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bool",
				"name": "open",
				"type": "bool"
			}
		],
		"name": "toggleBetting",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_feeRecipient",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "admin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "betsTeamA",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "betsTeamB",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "bettingOpen",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "feeRecipient",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAdmins",
		"outputs": [
			{
				"internalType": "address",
				"name": "contractAdmin",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "feeReceiver",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "bettor",
				"type": "address"
			}
		],
		"name": "getBetDetails",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "betTeamA",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "betTeamB",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getOutcome",
		"outputs": [
			{
				"internalType": "enum Betting.Outcome",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTotalBets",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "totalBetsA",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "totalBetsB",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "outcome",
		"outputs": [
			{
				"internalType": "enum Betting.Outcome",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalBetsTeamA",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalBetsTeamB",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]""" 



contract = w3.eth.contract(address=contract_address, abi=contract_abi)

st.title('Betting App')

private_key = st.text_input('Your Ethereum Private Key', type="password")  
account = w3.eth.account.privateKeyToAccount(private_key).address

outcome = contract.functions.getOutcome().call()
betting_open = contract.functions.bettingOpen().call()
total_bets_teamA, total_bets_teamB = contract.functions.getTotalBets().call()

st.write(f"Outcome: {outcome}")
st.write(f"Betting Open: {betting_open}")
st.write(f"Total Bets for Team A: {total_bets_teamA}")
st.write(f"Total Bets for Team B: {total_bets_teamB}")

bet_team = st.radio("Select Team", ["Team A", "Team B"])
amount = st.text_input('Bet Amount (ETH)')

if st.button("Place Bet"):
    nonce = w3.eth.getTransactionCount(account)
    if bet_team == "Team A":
        tx = contract.functions.placeBet(True).buildTransaction({
            'from': account,
            'value': w3.toWei(amount, 'ether'),
            'gas': 2000000,  # You may need to adjust
            'gasPrice': w3.toWei('20', 'gwei'),
            'nonce': nonce,
        })
    else:
        tx = contract.functions.placeBet(False).buildTransaction({
            'from': account,
            'value': w3.toWei(amount, 'ether'),
            'gas': 2000000,  # You may need to adjust
            'gasPrice': w3.toWei('20', 'gwei'),
            'nonce': nonce,
        })
    
    signed_tx = w3.eth.account.signTransaction(tx, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    st.write(f"Transaction Hash: {tx_hash.hex()}")

if st.button("Claim Winnings"):
    nonce = w3.eth.getTransactionCount(account)
    tx = contract.functions.claimWinnings().buildTransaction({
        'from': account,
        'gas': 2000000,  # You may need to adjust
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = w3.eth.account.signTransaction(tx, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    st.write(f"Transaction Hash: {tx_hash.hex()}")

st.sidebar.write("Warning: Never enter your real private key in any website or application!")

if __name__ == '__main__':
    st.write("Developed using Streamlit and web3.py")
