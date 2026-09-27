-- Microsoft SQL Server: tabel dan data hasil scoring risiko kredit
-- Dihasilkan oleh score_applications.py dari test_applications.csv

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'loan_risk_scores' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.loan_risk_scores (
        app_id            VARCHAR(20)     NOT NULL PRIMARY KEY,
        risk_score        INT             NOT NULL,
        risk_category     VARCHAR(10)     NOT NULL,
        credit_to_income  DECIMAL(10, 2)  NULL,
        data_flag         VARCHAR(200)    NULL,
        needs_review      BIT             NOT NULL,
        explanation       NVARCHAR(500)   NULL,
        scored_at         DATETIME2       NOT NULL DEFAULT SYSUTCDATETIME()
    );
END;
GO

INSERT INTO dbo.loan_risk_scores (app_id, risk_score, risk_category, credit_to_income, data_flag, needs_review, explanation)
VALUES
('APP-001', 11, 'Low', 2.00, NULL, 0, N'Profil risiko pemohon berada pada level rendah, terutama dipengaruhi oleh skor eksternal (EXT_SOURCE_2) rendah sebesar 0.72.'),
('APP-002', 100, 'High', 7.00, NULL, 1, N'Profil risiko pemohon berada pada level tinggi, terutama dipengaruhi oleh skor eksternal (EXT_SOURCE_2) rendah sebesar 0.18 dan rasio cicilan kredit terhadap pendapatan yang sangat tinggi (7.0x).'),
('APP-003', 80, 'High', 6.00, NULL, 1, N'Profil risiko pemohon berada pada level tinggi, terutama dipengaruhi oleh skor eksternal (EXT_SOURCE_2) rendah sebesar 0.25 dan rasio cicilan kredit terhadap pendapatan yang sangat tinggi (6.0x).'),
('APP-004', 54, 'Medium', 3.50, NULL, 0, N'Profil risiko pemohon berada pada level menengah, terutama dipengaruhi oleh skor eksternal (EXT_SOURCE_2) rendah sebesar 0.35 dan status tempat tinggal yang belum mandiri (rented apartment).'),
('APP-005', 92, 'High', 6.25, NULL, 1, N'Profil risiko pemohon berada pada level tinggi, terutama dipengaruhi oleh skor eksternal (EXT_SOURCE_2) rendah sebesar 0.20 dan rasio cicilan kredit terhadap pendapatan yang sangat tinggi (6.2x).'),
('APP-006', 20, 'Low', 2.00, 'EXT_SOURCE_2 kosong - wajib review manual', 1, N'Profil risiko pemohon berada pada level rendah, terutama dipengaruhi oleh skor eksternal (EXT_SOURCE_2) tidak tersedia sehingga dinilai netral-berisiko.');
GO
