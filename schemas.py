"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Brand-specific schemas

class Fragrance(BaseModel):
    slug: str = Field(..., description="URL-friendly identifier")
    name: str = Field(..., description="Fragrance name")
    tagline: Optional[str] = Field(None, description="Short tagline")
    color: str = Field(..., description="Primary HEX color for UI accents")
    description: str = Field(..., description="Detailed description")
    notes_top: List[str] = Field(default_factory=list, description="Top notes")
    notes_heart: List[str] = Field(default_factory=list, description="Heart notes")
    notes_base: List[str] = Field(default_factory=list, description="Base notes")
    ingredients: List[str] = Field(default_factory=list, description="Ingredients list")
    hero_image: Optional[str] = Field(None, description="Hero image URL")
    pack_image: Optional[str] = Field(None, description="Packaging image URL")
    is_active: bool = Field(True, description="Visibility toggle")

class Review(BaseModel):
    fragrance_slug: str = Field(..., description="Related fragrance slug")
    author: str = Field(..., description="Reviewer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating 1-5")
    content: str = Field(..., description="Review text")

class BlogPost(BaseModel):
    slug: str = Field(..., description="URL slug")
    title: str = Field(..., description="Post title")
    excerpt: Optional[str] = Field(None, description="Short summary")
    content: str = Field(..., description="HTML/Markdown content")
    cover_image: Optional[str] = Field(None, description="Cover image URL")
    tags: List[str] = Field(default_factory=list, description="Tags")
    published_at: Optional[datetime] = Field(None, description="Publication date")
    is_published: bool = Field(True)

class ContactMessage(BaseModel):
    name: str = Field(...)
    email: EmailStr
    phone: Optional[str] = None
    subject: str = Field(...)
    message: str = Field(..., min_length=5)

# Example schemas retained for reference
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True

