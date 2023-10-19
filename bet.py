# main.py
import streamlit as st
from web3 import Web3

# Connect to an Ethereum node (e.g., Ganache)
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

# Contract address and ABI
contract_address = "0xYourContractAddress" # Replace with contract address
contract_abi = [YourContractABI]  # Replace with the actual ABI

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

st.title("Binary Betting with Ethereum")

if st.button("Bet on Outcome"):
    outcome = st.radio("Select an outcome:", ("Option A", "Option B"))
    bet_amount = st.number_input("Enter your bet amount (in Ether):", 0.1, 10.0, 0.1)

    if st.button("Place Bet"):
        # Convert outcome to binary
        binary_outcome = outcome == "Option A"

        # Prepare the transaction
        transaction = contract.functions.bet(binary_outcome).buildTransaction(
            {
                "chainId": 1337,  # Replace with your network ID
                "gas": 2000000,  # Adjust gas as needed
                "gasPrice": w3.toWei("20", "gwei"),  # Adjust gas price as needed
                "nonce": w3.eth.getTransactionCount(w3.eth.accounts[0]),
            }
        )

        # Sign and send the transaction
        signed_transaction = w3.eth.account.signTransaction(transaction, private_key="YourPrivateKey")
        tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        st.write("Transaction sent. Waiting for confirmation...")
        st.write(f"Transaction hash: {tx_hash.hex()}")

if st.button("Claim Reward"):
    # Check if the user has won
    has_won = contract.functions.bets(w3.eth.accounts[0]).call()

    if has_won == 1:
        st.write("You have won! Claim your reward.")
        if st.button("Claim"):
            transaction = contract.functions.claimReward().buildTransaction(
                {
                    "chainId": 1337,  # Replace with your network ID
                    "gas": 2000000,  # Adjust gas as needed
                    "gasPrice": w3.toWei("20", "gwei"),  # Adjust gas price as needed
                    "nonce": w3.eth.getTransactionCount(w3.eth.accounts[0]),
                }
            )

            signed_transaction = w3.eth.account.signTransaction(transaction, private_key="YourPrivateKey")
            tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

            st.write("Transaction sent. Waiting for confirmation...")
            st.write(f"Transaction hash: {tx_hash.hex()}")
