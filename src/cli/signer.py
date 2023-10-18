"""
signer.py

Functions to be used during `sign` (sign function)
and `verify` (on_verify) operations.
"""
from utils.log import build_logger 
import hashlib

from utils.pem import create_public_key_certificate
from utils.qr import make_qr_code
from utils.video import scan_signature, scan_public_key


class Signer:
    """
    Signer is the class
    that manages the `sign` command

    Workflow:
        
    (1) Read a file;
    (2) Save in a .sha256.txt file;
    (3) Requires the user loads a xpriv key on his/her device:
        (a) load a 12/24 words key;
        (b) with or without BIP39 password;
    (4) sign a message:
        (a) once loaded the xpriv key, user goes
            to Sign > Message feature on his/her device
        (b) show a qrcode on device;
        (c) this function will generate a qrcode on computer;
        (d) once shown, the user will be prompted to scan it with device;
        (e) once scanned, the device will show some qrcodes:
            (i) the signature as a qrcode;
            (ii) the public key;
        (f) once above qrcodes are scanned, the computer
            will generate a publickey certificate, in a compressed
            or uncompressed format, in name of an owner.
    """
    
    def __init__(self, **kwargs):
        self.file = kwargs.get('file')
        self.owner = kwargs.get('owner')
        self.uncompressed = kwargs.get('uncompressed')
        self.log = build_logger(__name__, kwargs.get('loglevel'))

    def sign(self):
        self._show_warning_messages()
        data = self._hash_file()
        self._save_hash_file(data)
        self._print_qrcode(data)
        self._make_sig()

    def _show_warning_messages(self):
        """
        Shows warning messages before hash
        """
        self.log.debug('Showing warning messages to sign')        
        
        # Shows some message
        print("")
        print("To sign this file with Krux: ")
        print(" (a) load a 12/24 words key with or without password;")
        print(" (b) use the Sign->Message feature;")
        print(" (c) and scan this QR code below.")
        print("")

    def _hash_file(self) -> str:
        """
        Creates a hash file before sign
        """ 
        self.log.debug(f'Opening {self.file}')
        
        try:
            with open(self.file, "rb") as f_sig:
                self.log.debug('Reading bytes...')
                _bytes = f_sig.read() 

                self.log.debug('Hashing...')
                data = hashlib.sha256(_bytes).hexdigest()
                
                self.log.debug(f'Hash (data={data})')
                return data
        
        except FileNotFoundError as exc:
            message = f'Unable to read target file: {self.file}'
            numeric_level = getattr(logging, loglevel.upper(), None)
            if numeric_level == logging.NOTSET:
                 raise FileNotFoundError(message) from exc
            else:
                logging.error(message)
        
        return open_and_hash_file(path=self.file)

    def _save_hash_file(self, data): 
        """
        Save the hash file in sha256sum format
        """
        # Saves a hash file
        try:
            __hash_file__ = f"{self.file}.sha256sum.txt"
            self.log.debug(f'Saving {self.file}.sha256.txt')
        
            with open(__hash_file__, mode="w", encoding="utf-8") as hash_file:
                content = f'{data} {self.file}'
            
                self.log.debug(f'Saving content (data={content}')
                hash_file.write(content)

                self.log.debug(f'{__hash_file__} saved')
        
        except Exception as exc:
            message = f'Unknow error on saving {__hash_file__}'
            numeric_level = getattr(logging, loglevel.upper(), None)
            if numeric_level == logging.NOTSET:
                raise Exception(message) from exc
            else:
                logging.error(message)

    def _print_qrcode(self, data):
        """
        Print QRCode to console
        """
        # Prints the QR code
        self.log.debug(f"Creating QRCode (data={data})")
        __qrcode__ = make_qr_code(data=data)
        print(f"{__qrcode__}")

    def _make_sig(self):
        """
        Make signature file from scanning qrcode
        """
        # Scans the signature QR code
        self.log.debug('Creating signature')
        signature = scan_signature()
        
        # Saves a signature
        signature_file = f"{self.file}.sig"
        self.log.debug(f'Saving {signature_file}')

        try:
            with open(signature_file, "wb") as sig_file:
                sig_file.write(binary_signature)
                self.log.debug(f"Signature saved on {signature_file}")
    
        except Exception as exc:
            message = f'Unknow error on saving {__hash_file__}'
            numeric_level = getattr(logging, loglevel.upper(), None)
            if numeric_level == logging.NOTSET:
                raise Exception(message) from exc
            else:
                logging.error(message)

    def _make_pubkey_certificate(self):
        """
        Make public key file from scanning qrcode 
        """
        # Scans the public KeyboardInterruptardInterrupt
        self.log.debug('Creating public key')
        pubkey = scan_public_key()

        # Create PEM data
        # Save PEM data to a file
        # with filename as owner's name
        hex_pubkey = hex_pubkey.upper()

        # Choose if will be compressed or uncompressed
        if uncompressed:
            __public_key_data__ = f"{KSIGNER_UNCOMPRESSED_PUBKEY_PREPEND}{hex_pubkey}"
        else:
            __public_key_data__ = f"{KSIGNER_COMPRESSED_PUBKEY_PREPEND}{hex_pubkey}"

        # Convert pubkey data to bytes
        __public_key_data_bytes__ = bytes.fromhex(__public_key_data__)
        __public_key_data_b64__ = base64.b64encode(__public_key_data_bytes__)
        __public_key_data_b64__ = __public_key_data_b64__.decode("utf8")
        __public_key_name__ = f'{self.owner}.pem'

        try:
            with open(__public_key__name, 'wb') as pb_file:
                self.log.debug(f'Saving {__public_key_name__}')
                pb_file.write(__public_key_data_b64__)
                self.log.debug(f'{__public_key_name__} saved')
        
        except Exception as exc:
            message = f'Unknow error on saving {__hash_file__}'
            numeric_level = getattr(logging, loglevel.upper(), None)
            if numeric_level == logging.NOTSET:
                raise Exception(message) from exc
            else:
                logging.error(message)