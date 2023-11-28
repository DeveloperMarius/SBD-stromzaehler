/*
  Warnings:

  - You are about to drop the column `name` on the `User` table. All the data in the column will be lost.
  - Added the required column `nachname` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `vorname` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "User" DROP COLUMN "name",
ADD COLUMN     "nachname" TEXT NOT NULL,
ADD COLUMN     "vorname" TEXT NOT NULL;
