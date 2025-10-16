"""
AI-powered natural language query interface
"""
import os
from typing import Dict, Any, Optional
from datetime import datetime


class AIAssistant:
    """
    AI-powered assistant for natural language queries about stocks
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Assistant
        
        Args:
            api_key: OpenAI API key (optional, can use environment variable)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.chat_history = []
        
        # Check if OpenAI is available
        try:
            if self.api_key:
                from langchain_openai import ChatOpenAI
                from langchain.schema import HumanMessage, SystemMessage, AIMessage
                
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    openai_api_key=self.api_key
                )
                self.has_ai = True
                self.HumanMessage = HumanMessage
                self.SystemMessage = SystemMessage
                self.AIMessage = AIMessage
            else:
                self.has_ai = False
        except ImportError:
            self.has_ai = False
    
    def query(self, 
             question: str, 
             context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process a natural language query about stocks
        
        Args:
            question: User's question
            context: Additional context (stock data, indicators, etc.)
            
        Returns:
            AI-generated response
        """
        if not self.has_ai:
            return self._fallback_response(question, context)
        
        # Build context string
        context_str = ""
        if context:
            context_str = "\n\nContext:\n"
            for key, value in context.items():
                context_str += f"{key}: {value}\n"
        
        # Create system message
        system_msg = self.SystemMessage(content="""You are a professional stock market analyst and financial advisor. 
        You provide clear, accurate, and actionable insights about stocks based on technical analysis. 
        Your responses should be:
        - Professional and informative
        - Based on technical indicators when available
        - Include specific numbers and data points
        - Provide clear buy/sell/hold recommendations when asked
        - Explain technical terms in simple language when needed
        
        Always remind users that this is not financial advice and they should do their own research.""")
        
        # Create user message
        user_msg = self.HumanMessage(content=f"{question}{context_str}")
        
        # Add to history
        messages = [system_msg] + self.chat_history[-10:] + [user_msg]  # Keep last 10 messages for context
        
        try:
            # Get response
            response = self.llm.invoke(messages)
            
            # Update history
            self.chat_history.append(user_msg)
            self.chat_history.append(self.AIMessage(content=response.content))
            
            return response.content
        
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def _fallback_response(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Provide a fallback response when AI is not available
        
        Args:
            question: User's question
            context: Additional context
            
        Returns:
            Fallback response
        """
        response = "AI Assistant is not configured. Please set OPENAI_API_KEY environment variable.\n\n"
        
        if context:
            response += "However, here's the available data:\n\n"
            for key, value in context.items():
                response += f"{key}:\n{value}\n\n"
        
        return response
    
    def analyze_stock(self, 
                     stock_data: Dict[str, Any],
                     indicators: Dict[str, Any],
                     signals: Dict[str, Any]) -> str:
        """
        Generate comprehensive stock analysis
        
        Args:
            stock_data: Basic stock information
            indicators: Technical indicators
            signals: Buy/sell signals
            
        Returns:
            Comprehensive analysis
        """
        context = {
            "Stock Information": stock_data,
            "Technical Indicators": indicators,
            "Trading Signals": signals
        }
        
        question = f"Provide a comprehensive technical analysis for {stock_data.get('symbol', 'this stock')}. Include trend analysis, momentum indicators, and a clear recommendation."
        
        return self.query(question, context)
    
    def explain_indicator(self, indicator_name: str, value: float) -> str:
        """
        Explain what an indicator means
        
        Args:
            indicator_name: Name of the indicator
            value: Current value
            
        Returns:
            Explanation
        """
        question = f"Explain what {indicator_name} means in stock trading, and interpret a current value of {value}. Keep it simple and practical."
        
        return self.query(question)
    
    def portfolio_advice(self, 
                        portfolio_summary: Dict[str, Any],
                        market_conditions: Optional[str] = None) -> str:
        """
        Get portfolio management advice
        
        Args:
            portfolio_summary: Portfolio summary data
            market_conditions: Current market conditions description
            
        Returns:
            Portfolio advice
        """
        context = {
            "Portfolio Summary": portfolio_summary
        }
        
        if market_conditions:
            context["Market Conditions"] = market_conditions
        
        question = "Based on my portfolio, provide advice on diversification, risk management, and potential adjustments I should consider."
        
        return self.query(question, context)
    
    def compare_stocks(self, 
                      stocks_data: Dict[str, Dict[str, Any]]) -> str:
        """
        Compare multiple stocks
        
        Args:
            stocks_data: Dictionary of {symbol: data}
            
        Returns:
            Comparison analysis
        """
        context = {
            "Stocks Comparison": stocks_data
        }
        
        symbols = list(stocks_data.keys())
        question = f"Compare these stocks: {', '.join(symbols)}. Which one looks better for investment based on technical analysis? Provide a clear ranking and reasoning."
        
        return self.query(question, context)
    
    def clear_history(self) -> None:
        """
        Clear chat history
        """
        self.chat_history = []
    
    def get_chat_history(self) -> list:
        """
        Get chat history
        
        Returns:
            List of messages
        """
        return self.chat_history.copy()
