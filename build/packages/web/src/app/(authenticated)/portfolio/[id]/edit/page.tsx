"use client";

import { useParams } from "next/navigation";
import { Loader2 } from "lucide-react";
import { PortfolioForm } from "@/components/portfolio/PortfolioForm";
import { MilestoneList } from "@/components/portfolio/MilestoneList";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { usePortfolioItem } from "@/hooks/usePortfolioItems";

export default function PortfolioEditPage() {
  const params = useParams<{ id: string }>();
  const { data: item, isLoading, error } = usePortfolioItem(params.id);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-12">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (error || !item) {
    return (
      <div className="p-12 text-center">
        <p className="text-destructive">Failed to load portfolio item.</p>
      </div>
    );
  }

  return (
    <PortfolioForm initialData={item}>
      <Accordion type="multiple" defaultValue={["milestones"]}>
        <AccordionItem value="milestones">
          <AccordionTrigger>Milestones</AccordionTrigger>
          <AccordionContent className="pt-4">
            <MilestoneList portfolioItemId={item.id} milestones={item.milestones || []} />
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </PortfolioForm>
  );
}
