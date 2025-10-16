"""
Portfolio tracking and management module
"""
import pandas as pd
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import os


class PortfolioTracker:
    """
    Track and manage stock portfolio with positions and performance
    """
    
    def __init__(self, portfolio_file: str = 'portfolio.json'):
        """
        Initialize PortfolioTracker
        
        Args:
            portfolio_file: Path to portfolio data file
        """
        self.portfolio_file = portfolio_file
        self.positions = {}
        self.transactions = []
        self.load_portfolio()
    
    def load_portfolio(self) -> None:
        """
        Load portfolio from file
        """
        if os.path.exists(self.portfolio_file):
            try:
                with open(self.portfolio_file, 'r') as f:
                    data = json.load(f)
                    self.positions = data.get('positions', {})
                    self.transactions = data.get('transactions', [])
            except Exception as e:
                print(f"Error loading portfolio: {e}")
                self.positions = {}
                self.transactions = []
        else:
            self.positions = {}
            self.transactions = []
    
    def save_portfolio(self) -> None:
        """
        Save portfolio to file
        """
        data = {
            'positions': self.positions,
            'transactions': self.transactions,
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.portfolio_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving portfolio: {e}")
    
    def add_position(self, 
                    symbol: str, 
                    quantity: float, 
                    purchase_price: float,
                    purchase_date: Optional[str] = None) -> None:
        """
        Add a new position or update existing position
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            purchase_price: Price per share at purchase
            purchase_date: Date of purchase (ISO format)
        """
        symbol = symbol.upper()
        
        if purchase_date is None:
            purchase_date = datetime.now().isoformat()
        
        # Add transaction
        transaction = {
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': purchase_price,
            'date': purchase_date,
            'total': quantity * purchase_price
        }
        self.transactions.append(transaction)
        
        # Update position
        if symbol in self.positions:
            # Update average price
            current_qty = self.positions[symbol]['quantity']
            current_avg_price = self.positions[symbol]['avg_price']
            
            new_qty = current_qty + quantity
            new_avg_price = ((current_qty * current_avg_price) + 
                           (quantity * purchase_price)) / new_qty
            
            self.positions[symbol]['quantity'] = new_qty
            self.positions[symbol]['avg_price'] = new_avg_price
        else:
            self.positions[symbol] = {
                'quantity': quantity,
                'avg_price': purchase_price,
                'first_purchase_date': purchase_date
            }
        
        self.save_portfolio()
    
    def remove_position(self, 
                       symbol: str, 
                       quantity: float, 
                       sale_price: float,
                       sale_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Remove or reduce a position (sell shares)
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to sell
            sale_price: Price per share at sale
            sale_date: Date of sale (ISO format)
            
        Returns:
            Dictionary with sale information including profit/loss
        """
        symbol = symbol.upper()
        
        if symbol not in self.positions:
            raise ValueError(f"No position found for {symbol}")
        
        if self.positions[symbol]['quantity'] < quantity:
            raise ValueError(f"Insufficient shares. Current quantity: {self.positions[symbol]['quantity']}")
        
        if sale_date is None:
            sale_date = datetime.now().isoformat()
        
        avg_price = self.positions[symbol]['avg_price']
        profit_loss = (sale_price - avg_price) * quantity
        profit_loss_pct = ((sale_price - avg_price) / avg_price) * 100
        
        # Add transaction
        transaction = {
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': sale_price,
            'date': sale_date,
            'total': quantity * sale_price,
            'profit_loss': profit_loss,
            'profit_loss_pct': profit_loss_pct
        }
        self.transactions.append(transaction)
        
        # Update position
        self.positions[symbol]['quantity'] -= quantity
        
        # Remove position if quantity is 0
        if self.positions[symbol]['quantity'] == 0:
            del self.positions[symbol]
        
        self.save_portfolio()
        
        return transaction
    
    def get_positions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all current positions
        
        Returns:
            Dictionary of positions
        """
        return self.positions.copy()
    
    def get_position_value(self, symbol: str, current_price: float) -> Dict[str, Any]:
        """
        Get current value and performance of a position
        
        Args:
            symbol: Stock symbol
            current_price: Current market price
            
        Returns:
            Dictionary with position value and performance
        """
        symbol = symbol.upper()
        
        if symbol not in self.positions:
            raise ValueError(f"No position found for {symbol}")
        
        position = self.positions[symbol]
        quantity = position['quantity']
        avg_price = position['avg_price']
        
        current_value = quantity * current_price
        cost_basis = quantity * avg_price
        profit_loss = current_value - cost_basis
        profit_loss_pct = (profit_loss / cost_basis) * 100
        
        return {
            'symbol': symbol,
            'quantity': quantity,
            'avg_price': avg_price,
            'current_price': current_price,
            'cost_basis': cost_basis,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_pct': profit_loss_pct
        }
    
    def get_portfolio_summary(self, current_prices: Dict[str, float]) -> Dict[str, Any]:
        """
        Get overall portfolio summary
        
        Args:
            current_prices: Dictionary of {symbol: current_price}
            
        Returns:
            Portfolio summary with total value and performance
        """
        total_value = 0
        total_cost = 0
        positions_summary = []
        
        for symbol in self.positions:
            if symbol in current_prices:
                position_value = self.get_position_value(symbol, current_prices[symbol])
                positions_summary.append(position_value)
                total_value += position_value['current_value']
                total_cost += position_value['cost_basis']
        
        total_profit_loss = total_value - total_cost
        total_profit_loss_pct = (total_profit_loss / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'total_positions': len(self.positions),
            'total_value': total_value,
            'total_cost': total_cost,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_pct': total_profit_loss_pct,
            'positions': positions_summary
        }
    
    def get_transaction_history(self, 
                               symbol: Optional[str] = None,
                               transaction_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get transaction history with optional filters
        
        Args:
            symbol: Filter by symbol (optional)
            transaction_type: Filter by type 'BUY' or 'SELL' (optional)
            
        Returns:
            List of transactions
        """
        transactions = self.transactions.copy()
        
        if symbol:
            symbol = symbol.upper()
            transactions = [t for t in transactions if t['symbol'] == symbol]
        
        if transaction_type:
            transaction_type = transaction_type.upper()
            transactions = [t for t in transactions if t['type'] == transaction_type]
        
        # Sort by date (most recent first)
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        return transactions
    
    def get_performance_metrics(self, current_prices: Dict[str, float]) -> Dict[str, Any]:
        """
        Get detailed performance metrics
        
        Args:
            current_prices: Dictionary of {symbol: current_price}
            
        Returns:
            Performance metrics
        """
        summary = self.get_portfolio_summary(current_prices)
        
        # Calculate realized gains from sell transactions
        realized_gains = sum(
            t.get('profit_loss', 0) 
            for t in self.transactions 
            if t['type'] == 'SELL'
        )
        
        # Best and worst performers
        positions = summary['positions']
        if positions:
            best_performer = max(positions, key=lambda x: x['profit_loss_pct'])
            worst_performer = min(positions, key=lambda x: x['profit_loss_pct'])
        else:
            best_performer = None
            worst_performer = None
        
        return {
            'unrealized_profit_loss': summary['total_profit_loss'],
            'unrealized_profit_loss_pct': summary['total_profit_loss_pct'],
            'realized_profit_loss': realized_gains,
            'total_profit_loss': summary['total_profit_loss'] + realized_gains,
            'best_performer': best_performer,
            'worst_performer': worst_performer,
            'total_transactions': len(self.transactions),
            'win_rate': self._calculate_win_rate()
        }
    
    def _calculate_win_rate(self) -> float:
        """
        Calculate win rate from sell transactions
        
        Returns:
            Win rate percentage
        """
        sell_transactions = [t for t in self.transactions if t['type'] == 'SELL']
        
        if not sell_transactions:
            return 0.0
        
        winning_trades = sum(1 for t in sell_transactions if t.get('profit_loss', 0) > 0)
        
        return (winning_trades / len(sell_transactions)) * 100
