-- DropForeignKey
ALTER TABLE "Powermeter" DROP CONSTRAINT "Powermeter_contractId_fkey";

-- AddForeignKey
ALTER TABLE "Powermeter" ADD CONSTRAINT "Powermeter_contractId_fkey" FOREIGN KEY ("contractId") REFERENCES "Contract"("id") ON DELETE CASCADE ON UPDATE CASCADE;
