-- Run this if upgrading an existing stock_data table that was created before Kafka integration.
-- The DAG's CREATE TABLE IF NOT EXISTS already includes these columns for fresh deployments.
ALTER TABLE stock_data
    ADD COLUMN IF NOT EXISTS predicted_close DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS rsi_14 DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS ma_5 DOUBLE PRECISION;
