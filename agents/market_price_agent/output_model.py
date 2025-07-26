from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class PriceUnit(str, Enum):
    """Enum for common price units in agricultural markets."""
    PER_KG = "per kg"
    PER_QUINTAL = "per quintal"
    PER_TON = "per ton"
    PER_TONNE = "per tonne"
    PER_POUND = "per pound"
    PER_BUSHEL = "per bushel"
    PER_CWT = "per cwt"
    PER_BAG = "per bag"
    PER_PIECE = "per piece"

class MarketInfo(BaseModel):
    """Individual market/mandi information."""
    market_name: Optional[str] = Field(None, description="Name of the market/mandi.")
    min_price: Optional[float] = Field(None, description="Minimum price as numerical value.")
    max_price: Optional[float] = Field(None, description="Maximum price as numerical value.")
    avg_price: Optional[float] = Field(None, description="Average price as numerical value.")
    modal_price: Optional[float] = Field(None, description="Modal/prevalent price as numerical value.")
    unit: Optional[str] = Field(None, description="Unit of measurement (per kg, per quintal, etc.).")
    date: Optional[str] = Field(None, description="Date of the price quote.")

class PriceSummary(BaseModel):
    """Overall price summary across all markets."""
    overall_min_price: Optional[float] = Field(None, description="Lowest minimum price across all markets.")
    overall_max_price: Optional[float] = Field(None, description="Highest maximum price across all markets.")
    weighted_avg_price: Optional[float] = Field(None, description="Weighted average price across markets.")
    price_range: Optional[float] = Field(None, description="Difference between max and min prices.")
    standard_unit: Optional[str] = Field(None, description="Standardized unit for all calculations.")

class CalculationResult(BaseModel):
    """Results from price calculations if requested."""
    calculation_type: Optional[str] = Field(None, description="Type of calculation performed.")
    input_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters used in calculation.")
    result: Optional[Dict[str, Union[float, str]]] = Field(None, description="Calculation results.")
    explanation: Optional[str] = Field(None, description="Explanation of the calculation.")

class MarketPriceAgentOutput(BaseModel):
    """Enhanced output model for Market Price Agent with calculation support."""
    
    # Basic search parameters
    crop: Optional[str] = Field(None, description="The crop searched for.")
    state: Optional[str] = Field(None, description="The state searched for.")
    district: Optional[str] = Field(None, description="The district searched for.")
    market: Optional[str] = Field(None, description="The specific market searched for.")
    
    # Legacy fields for backward compatibility
    min_market_price: Optional[str] = Field(None, description="The minimum market price as string (legacy).")
    max_market_price: Optional[str] = Field(None, description="The maximum market price as string (legacy).")
    
    # Enhanced price information
    price_summary: Optional[PriceSummary] = Field(None, description="Overall price summary with numerical values.")
    markets_data: Optional[List[MarketInfo]] = Field(default_factory=list, description="Detailed information for each market.")
    
    # Date and time information
    search_date: Optional[str] = Field(None, description="Date when the search was performed.")
    price_date: Optional[str] = Field(None, description="Date of the latest price data.")
    
    # Calculation support
    calculation_requested: bool = Field(False, description="Whether user requested calculations.")
    calculation_results: Optional[List[CalculationResult]] = Field(default_factory=list, description="Results of any calculations performed.")
    
    # Status and metadata
    search_successful: bool = Field(True, description="Whether the price search was successful.")
    data_availability: Optional[str] = Field(None, description="Information about data availability (current/recent/unavailable).")
    sources: Optional[List[str]] = Field(default_factory=list, description="Sources of price data.")
    
    # Response formatting
    full_response: str = Field(..., description="The complete response in proper sentences.")
    structured_data_available: bool = Field(False, description="Whether structured numerical data is available for calculations.")
    
    # Additional context
    market_trends: Optional[str] = Field(None, description="Brief information about market trends if available.")
    seasonal_context: Optional[str] = Field(None, description="Seasonal context affecting prices if relevant.")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True
        extra = "forbid"