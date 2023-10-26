import streamlit as st
from web3 import Web3

# Initialize Web3
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))  
contract_address = "0x8467364C3e1D318cD9a4150BD8Fb660f3E0307D9"  
abi = """[
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

contract = web3.eth.contract(address=contract_address, abi=abi)

# Streamlit App
st.title("Betting DApp")

# Define Streamlit functions to interact with the contract
def place_bet(for_team_a, amount):
    bet_in_wei = Web3.toWei(amount, 'ether')
    tx = {
        "from": web3.eth.defaultAccount,
        "value": bet_in_wei
    }
    contract.functions.placeBet(for_team_a).transact(tx)
    st.success("Bet placed successfully!")

def decide_outcome(team_a_won):
    tx = {"from": web3.eth.defaultAccount}
    contract.functions.decideOutcome(team_a_won).transact(tx)
    st.success("Outcome decided!")

def claim_winnings():
    tx = {"from": web3.eth.defaultAccount}
    contract.functions.claimWinnings().transact(tx)
    st.success("Winnings claimed!")

# Removed set_odds function as it was not in the provided contract

# Calculate potential winnings
def calculate_winnings(for_team_a, amount):
    if for_team_a:
        total_bets_other_team = contract.functions.totalBetsTeamB().call()
    else:
        total_bets_other_team = contract.functions.totalBetsTeamA().call()

    if total_bets_other_team == 0:
        return 0

    potential_winnings = (amount * total_bets_other_team) / (total_bets_other_team + amount)
    return potential_winnings

# User interface
st.sidebar.header("Place a Bet")
for_team_a = st.sidebar.radio("Bet for Team A or Team B:", ("Team A", "Team B"))
amount = st.sidebar.number_input("Bet Amount (in ETH)", min_value=0.0)

if st.sidebar.button("Place Bet"):
    place_bet(for_team_a == "Team A", amount)

st.sidebar.header("Admin Functions")
if st.sidebar.checkbox("Decide Outcome"):
    team_a_won = st.sidebar.radio("Did Team A win?", ("Yes", "No"))
    if st.sidebar.button("Decide"):
        decide_outcome(team_a_won == "Yes")

st.sidebar.header("Calculate Potential Winnings")
if st.sidebar.button("Calculate Potential Winnings"):
    potential_winnings = calculate_winnings(for_team_a == "Team A", amount)
    st.sidebar.write(f"Potential Winnings: {potential_winnings:.2f} ETH")

st.sidebar.header("Claim Winnings")
if st.sidebar.button("Claim Winnings"):
    claim_winnings()

st.sidebar.markdown("Note: You must have MetaMask or a compatible Ethereum wallet to use this DApp.")
st.sidebar.info("Connect your Ethereum wallet to interact with the contract.")

# Display contract data
st.write("Contract Data")
st.write(f"Admin Address: {contract.functions.admin().call()}")
st.write(f"Outcome: {contract.functions.getOutcome().call()}")
st.write(f"Total Bets on Team A: {contract.functions.totalBetsTeamA().call()} ETH")
st.write(f"Total Bets on Team B: {contract.functions.totalBetsTeamB().call()} ETH")
