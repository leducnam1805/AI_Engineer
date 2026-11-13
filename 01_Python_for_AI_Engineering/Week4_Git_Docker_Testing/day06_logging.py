"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 4 - NGÀY 6: Structured Logging cho AI Apps   ║
║  Logging JSON format, Request Tracing                        ║
╚══════════════════════════════════════════════════════════════╝
"""

import logging
import json
from datetime import datetime

# Cấu hình logging chuẩn JSON (Rất quan trọng khi đẩy log lên Datadog, ELK, Grafana Loki)
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName
        }
        if hasattr(record, "extra_info"):
            log_obj["extra"] = record.extra_info
        return json.dumps(log_obj)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger("ai_service")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Test log
logger.info("Khởi động AI Backend Service thành công!")
logger.warning("Cảnh báo: Request có latency cao hơn 1000ms")

