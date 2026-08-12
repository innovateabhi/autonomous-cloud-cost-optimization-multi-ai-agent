from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Numeric,
    BigInteger,
    ForeignKey,
    Text
)

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import declarative_base


# ============================================================
# BASE
# ============================================================

Base = declarative_base()


# ============================================================
# RESOURCE
# ============================================================

class Resource(Base):

    __tablename__ = "resources"

    id = Column(
        Integer,
        primary_key=True
    )

    resource_id = Column(
        String(255),
        nullable=False
    )

    resource_type = Column(
        String(50),
        nullable=False
    )

    name = Column(
        String(255)
    )

    region = Column(
        String(50),
        nullable=False
    )

    state = Column(
        String(50)
    )

    instance_type = Column(
        String(100)
    )

    environment = Column(
        String(50)
    )

    tags = Column(
        JSONB
    )

    discovered_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# METRIC
# ============================================================

class Metric(Base):

    __tablename__ = "metrics"

    id = Column(
        Integer,
        primary_key=True
    )

    resource_id = Column(
        Integer,
        ForeignKey(
            "resources.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    cpu_average = Column(
        Numeric(10, 4)
    )

    cpu_maximum = Column(
        Numeric(10, 4)
    )

    cpu_minimum = Column(
        Numeric(10, 4)
    )

    network_in = Column(
        BigInteger
    )

    network_out = Column(
        BigInteger
    )

    disk_read = Column(
        BigInteger
    )

    disk_write = Column(
        BigInteger
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# COST
# ============================================================

class Cost(Base):

    __tablename__ = "costs"

    id = Column(
        Integer,
        primary_key=True
    )

    resource_id = Column(
        Integer,
        ForeignKey(
            "resources.id",
            ondelete="SET NULL"
        )
    )

    service = Column(
        String(255),
        nullable=False
    )

    cost_date = Column(
        Date,
        nullable=False
    )

    amount = Column(
        Numeric(14, 6),
        nullable=False
    )

    currency = Column(
        String(10),
        default="USD"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# RECOMMENDATION
# ============================================================

class Recommendation(Base):

    __tablename__ = "recommendations"

    id = Column(
        Integer,
        primary_key=True
    )

    resource_id = Column(
        Integer,
        ForeignKey(
            "resources.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    recommendation_type = Column(
        String(100),
        nullable=False
    )

    current_configuration = Column(
        JSONB
    )

    recommended_configuration = Column(
        JSONB
    )

    estimated_monthly_savings = Column(
        Numeric(14, 6)
    )

    currency = Column(
        String(10),
        default="USD"
    )

    risk_level = Column(
        String(20)
    )

    reason = Column(
        Text
    )

    confidence = Column(
        Numeric(5, 2)
    )

    status = Column(
        String(30),
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    reviewed_at = Column(
        DateTime
    )


# ============================================================
# ACTION
# ============================================================

class Action(Base):

    __tablename__ = "actions"

    id = Column(
        Integer,
        primary_key=True
    )

    recommendation_id = Column(
        Integer,
        ForeignKey(
            "recommendations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    action_type = Column(
        String(100),
        nullable=False
    )

    executed_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    status = Column(
        String(30)
    )

    result = Column(
        Text
    )

    error_message = Column(
        Text
    )

    approved_by = Column(
        String(255)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# AUDIT LOG
# ============================================================

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    resource_id = Column(
        Integer,
        ForeignKey(
            "resources.id",
            ondelete="SET NULL"
        )
    )

    recommendation_id = Column(
        Integer,
        ForeignKey(
            "recommendations.id",
            ondelete="SET NULL"
        )
    )

    action_id = Column(
        Integer,
        ForeignKey(
            "actions.id",
            ondelete="SET NULL"
        )
    )

    event_type = Column(
        String(100),
        default="ANALYSIS"
    )

    agent_name = Column(
        String(100)
    )

    recommendation = Column(
        String(100)
    )

    priority = Column(
        String(30)
    )

    risk_level = Column(
        String(20)
    )

    decision = Column(
        String(100)
    )

    execution_action = Column(
        String(100)
    )

    execution_status = Column(
        String(30)
    )

    estimated_savings = Column(
        Numeric(14, 6)
    )

    llm_status = Column(
        String(30)
    )

    llm_model = Column(
        String(100)
    )

    llm_recommendation = Column(
        Text
    )

    confidence = Column(
        Numeric(5, 2)
    )

    status = Column(
        String(30)
    )

    details = Column(
        JSONB
    )

    message = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
