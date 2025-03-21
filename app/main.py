import asyncio
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.types import FSInputFile
import os
from datetime import datetime
import logging
import tempfile
import pathlib
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

def decode_email_subject(subject):
    """Decode email subject from various encodings"""
    if not subject:
        return "No Subject"
    decoded_list = decode_header(subject)
    subject = ""
    for content, encoding in decoded_list:
        if isinstance(content, bytes):
            if encoding:
                subject += content.decode(encoding)
            else:
                subject += content.decode()
        else:
            subject += content
    return subject

def get_email_content(email_message):
    """Extract text content from email"""
    try:
        text_content = ""
        html_content = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        text_content = payload.decode()
                elif part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        html_content = payload.decode()
        else:
            if email_message.get_content_type() == "text/plain":
                payload = email_message.get_payload(decode=True)
                if payload:
                    text_content = payload.decode()
            elif email_message.get_content_type() == "text/html":
                payload = email_message.get_payload(decode=True)
                if payload:
                    html_content = payload.decode()
        
        # If we have plain text, use it
        if text_content:
            return text_content.strip()
        
        # If we have HTML, convert it to plain text
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator='\n', strip=True)
        
        return "No text content found"
    except Exception as e:
        logger.error(f"Error getting email content: {e}")
        return "Error extracting email content"

def get_email_attachments(email_message):
    """Extract attachments from email"""
    attachments = []
    try:
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename:
                    filename = decode_header(filename)[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode()
                    payload = part.get_payload(decode=True)
                    if payload:
                        attachments.append((filename, payload))
    except Exception as e:
        logger.error(f"Error getting attachments: {e}")
    return attachments

async def check_new_emails():
    """Check for new emails and send them to Telegram"""
    try:
        imap = imaplib.IMAP4_SSL(settings.MAIL_SERVER)
        imap.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        
        # Select inbox
        imap.select("INBOX")
        
        # Search for unread emails
        _, message_numbers = imap.search(None, "UNSEEN")
        
        if not message_numbers or not message_numbers[0]:
            logger.info("No new emails found")
            return
            
        for num in message_numbers[0].split():
            try:
                _, msg_data = imap.fetch(num, "(RFC822)")
                if not msg_data or not msg_data[0] or not msg_data[0][1]:
                    logger.error(f"Empty message data for message {num}")
                    continue
                    
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Get email details
                subject = decode_email_subject(email_message.get("subject", ""))
                from_addr = email_message.get("from", "Unknown")
                date = email_message.get("date", "Unknown")
                
                # Get email content
                content = get_email_content(email_message)
                
                # Prepare message
                message = f"📧 New email received!\n\n"
                message += f"From: {from_addr}\n"
                message += f"Subject: {subject}\n"
                message += f"Date: {date}\n\n"
                message += f"Content:\n{content[:4000]}"  # Limit content length
                
                # Send text content to Telegram
                await bot.send_message(chat_id=settings.CHAT_ID, text=message)
                
                # Handle attachments
                attachments = get_email_attachments(email_message)
                for filename, content in attachments:
                    try:
                        if not content:
                            logger.warning(f"Empty content for attachment {filename}")
                            continue
                            
                        # Create a temporary directory
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Create a safe filename
                            safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))
                            file_path = os.path.join(temp_dir, safe_filename)
                            
                            # Save attachment
                            with open(file_path, "wb") as f:
                                f.write(content)
                            
                            # Send file to Telegram using FSInputFile
                            file = FSInputFile(file_path)
                            await bot.send_document(
                                chat_id=settings.CHAT_ID,
                                document=file,
                                caption=f"📎 Attachment: {safe_filename}"
                            )
                                
                    except Exception as e:
                        logger.error(f"Error sending attachment {filename}: {e}")
                        # Try to send error message to Telegram
                        try:
                            await bot.send_message(
                                chat_id=settings.CHAT_ID,
                                text=f"❌ Error sending attachment {filename}: {str(e)}"
                            )
                        except:
                            pass
                            
            except Exception as e:
                logger.error(f"Error processing message {num}: {e}")
                continue
            
    except Exception as e:
        logger.error(f"Error checking emails: {e}")
    finally:
        try:
            imap.close()
            imap.logout()
        except:
            pass

async def main():
    """Main function to run the bot"""
    while True:
        try:
            await check_new_emails()
            await asyncio.sleep(settings.CHECK_INTERVAL)  # Check every 5 minutes
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            await asyncio.sleep(settings.RETRY_INTERVAL)  # Wait a minute before retrying

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}") 