/*
  Warnings:

  - You are about to drop the `Reading` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Reading" DROP CONSTRAINT "Reading_powermeterId_fkey";

-- DropTable
DROP TABLE "Reading";
