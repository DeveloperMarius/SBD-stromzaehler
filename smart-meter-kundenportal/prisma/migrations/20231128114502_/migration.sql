/*
  Warnings:

  - Added the required column `blz` to the `Contract` table without a default value. This is not possible if the table is not empty.
  - Added the required column `hausnr` to the `Contract` table without a default value. This is not possible if the table is not empty.
  - Added the required column `iban` to the `Contract` table without a default value. This is not possible if the table is not empty.
  - Added the required column `ort` to the `Contract` table without a default value. This is not possible if the table is not empty.
  - Added the required column `plz` to the `Contract` table without a default value. This is not possible if the table is not empty.
  - Added the required column `strasse` to the `Contract` table without a default value. This is not possible if the table is not empty.
  - Added the required column `telefon` to the `Contract` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Contract" ADD COLUMN     "blz" TEXT NOT NULL,
ADD COLUMN     "hausnr" TEXT NOT NULL,
ADD COLUMN     "iban" TEXT NOT NULL,
ADD COLUMN     "ort" TEXT NOT NULL,
ADD COLUMN     "plz" TEXT NOT NULL,
ADD COLUMN     "strasse" TEXT NOT NULL,
ADD COLUMN     "telefon" TEXT NOT NULL;
