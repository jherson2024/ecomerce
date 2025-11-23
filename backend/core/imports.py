# imports.py
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import os
import bcrypt

# Recursos locales
from db import get_db
from core.security import get_password_hash, verify_password
from utils.keygen import generate_uint64_key
from utils.token_manager import generar_token
from core.globals import *
