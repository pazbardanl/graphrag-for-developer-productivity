package com.pazbarda.graphrag4devprod.prdata.models;

public enum PrStatus {
    OPEN,
    IN_REVIEW,
    CLOSED;

    public static PrStatus fromString(String status) {
        if (status == null) {
            return null;
        }
        try {
            return PrStatus.valueOf(status.toUpperCase());
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}
