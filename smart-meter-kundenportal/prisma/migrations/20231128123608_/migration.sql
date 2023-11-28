/*
  Warnings:

  - You are about to drop the column `powermeter` on the `Powermeter` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "Powermeter_powermeter_key";

-- AlterTable
ALTER TABLE "Powermeter" DROP COLUMN "powermeter";
