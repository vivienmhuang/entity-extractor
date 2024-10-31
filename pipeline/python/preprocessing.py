#/*************************************************************************************************
# Imports 
#/************************************************************************************************
import os
import logging
import pymupdf
import spacy
import regex as re
from typing import List, Dict

#/*************************************************************************************************
# Preprocessing scripts
#/*************************************************************************************************
def extract_text_from_pdf(file_path: str, logger: logging.Logger) -> str:
    """
    Extract text from a PDF file
    Args:
        file_path: Path to the PDF file
        logger: Logger instance from app.py
    Returns:
        Extracted text as string
    """
    logger.info(f"Starting text extraction from: {file_path}")
    try:
        doc = pymupdf.open(file_path)
        total_pages = len(doc)
        text = ""
        for page_num, page in enumerate(doc, 1):
            logger.debug(f"Processing page {page_num} out of {total_pages}")
            page_text = page.get_text()
            page_text = page_text.strip()
            text += page_text
        
        # Remove all newlines and hyphens
        text = text.replace('\r', '\n')
        text = text.replace('- ', '')

        logger.info(f"Successfully extracted {len(text)} characters")
        return text
    
    except Exception as e:
        logger.error(f"Failed to extract text: {str(e)}")
        raise
    
    finally:
        # Ensures doc is closed even if an error occurs during text extraction
        if 'doc' in locals():
            doc.close()
            logger.debug("Closed PDF document")

def get_entity_context(doc: object, ent: object, logger: logging.Logger, window_size=100):
    """
    Get context around an entity using sentence boundaries and preserve positions.
    
    Args:
        doc: spaCy Doc object
        ent: Entity span from spaCy
        window_size: Fallback window size if sentence boundaries not found
    
    Returns:
        dict: Context information with original positions
    """
    # Get entity's sentence
    sent = ent.sent if ent.sent else None
    
    if sent:
        # Use sentence boundaries for context
        context_start = sent.start_char
        context_end = sent.end_char
    else:
        # Fallback to character window if sentence boundary not found
        context_start = max(0, ent.start_char - window_size)
        context_end = min(len(doc.text), ent.end_char + window_size)
    
    # Extract context and clean it
    context = doc.text[context_start:context_end].strip()
    context = ' '.join(context.split()) # Splits on white spaces, newlines
    
    # Return expected json
    return {
        'text': ent.text,
        'start': ent.start_char,
        'end': ent.end_char,
        'context': context
    }

def extract_entities(text: str, logger: logging.Logger):
    """
    Extract scientific entities from text using a scispacy model. 
    For each entity, it extracts contextual information and position data.

    Args:
        text (str): The scientific text to process. Should be preprocessed and cleaned.
        logger (logging.Logger): Logger instance for tracking the extraction process.

    """
    # Load scispacy model
    try:
        nlp = spacy.load("en_core_sci_lg")
        logger.debug("Loaded 'en_core_sci_lg' scispacy model successfully")
    except:
        logger.error("Required model 'en_core_sci_lg' not found")
        raise

    # Extract entities and context
    try: 
        logger.info(f"Run text through 'en_core_sci_lg' scispacy model")
        doc = nlp(text)
        entities = []

        logger.info(f"Extracting entities")
        for ent in doc.ents:
            context_info = get_entity_context(doc, ent, logger)
            entities.append(context_info)

        logger.info(f"Successfully extracted {len(entities)} entities")
        return entities

    except Exception as e:
        logger.error(f"Error during entity extraction: {str(e)}")
        raise    