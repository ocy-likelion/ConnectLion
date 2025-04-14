import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { GraduationCap, Upload, FileText, Bell, Settings } from "lucide-react"

export default function GraduatePage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-xl">
            <GraduationCap className="h-6 w-6" />
            <Link href="/">TalentConnect</Link>
          </div>
          <nav className="flex items-center gap-6">
            <Link href="/graduate/profile" className="text-sm font-medium hover:underline flex items-center gap-1">
              <FileText className="h-4 w-4" />내 프로필
            </Link>
            <Link
              href="/graduate/notifications"
              className="text-sm font-medium hover:underline flex items-center gap-1"
            >
              <Bell className="h-4 w-4" />
              알림
            </Link>
            <Link href="/graduate/settings" className="text-sm font-medium hover:underline flex items-center gap-1">
              <Settings className="h-4 w-4" />
              설정
            </Link>
            <div className="h-8 w-8 rounded-full bg-muted overflow-hidden">
              <Image
                src="/placeholder.svg?height=32&width=32"
                alt="Profile"
                width={32}
                height={32}
                className="h-full w-full object-cover"
              />
            </div>
          </nav>
        </div>
      </header>
      <main className="flex-1">
        <div className="container py-8">
          <div className="grid gap-8 md:grid-cols-[300px_1fr]">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>내 프로필</CardTitle>
                  <CardDescription>포트폴리오와 정보를 관리하세요</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-col items-center gap-4">
                    <div className="h-24 w-24 rounded-full bg-muted overflow-hidden">
                      <Image
                        src="/placeholder.svg?height=96&width=96"
                        alt="Profile"
                        width={96}
                        height={96}
                        className="h-full w-full object-cover"
                      />
                    </div>
                    <div className="text-center">
                      <h3 className="font-medium">홍길동</h3>
                      <p className="text-sm text-muted-foreground">프론트엔드 개발자</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="text-sm font-medium">프로필 완성도</div>
                    <div className="h-2 rounded-full bg-muted overflow-hidden">
                      <div className="h-full w-3/4 bg-primary"></div>
                    </div>
                    <p className="text-xs text-muted-foreground">75% 완료됨</p>
                  </div>
                </CardContent>
                <CardFooter>
                  <Button className="w-full gap-2">
                    <Upload className="h-4 w-4" />
                    포트폴리오 업로드
                  </Button>
                </CardFooter>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>스카우트 현황</CardTitle>
                  <CardDescription>기업으로부터 받은 제안</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-medium">총 제안</div>
                      <div className="font-bold">3</div>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-medium">새 제안</div>
                      <div className="font-bold text-primary">1</div>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-medium">프로필 조회</div>
                      <div className="font-bold">27</div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <Button variant="outline" className="w-full">
                    모든 제안 보기
                  </Button>
                </CardFooter>
              </Card>
            </div>
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>포트폴리오 관리</CardTitle>
                  <CardDescription>채용 담당자가 쉽게 볼 수 있도록 포트폴리오를 구성하세요</CardDescription>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="projects">
                    <TabsList className="grid w-full grid-cols-3">
                      <TabsTrigger value="projects">프로젝트</TabsTrigger>
                      <TabsTrigger value="skills">기술 스택</TabsTrigger>
                      <TabsTrigger value="education">교육 및 경력</TabsTrigger>
                    </TabsList>
                    <TabsContent value="projects" className="space-y-4 pt-4">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium">내 프로젝트</h3>
                        <Button size="sm">프로젝트 추가</Button>
                      </div>
                      <div className="grid gap-4 md:grid-cols-2">
                        {[1, 2, 3, 4].map((project) => (
                          <Card key={project}>
                            <CardHeader className="p-4">
                              <div className="aspect-video bg-muted rounded-md overflow-hidden">
                                <Image
                                  src={`/placeholder.svg?height=180&width=320&text=Project+${project}`}
                                  alt={`Project ${project}`}
                                  width={320}
                                  height={180}
                                  className="h-full w-full object-cover"
                                />
                              </div>
                            </CardHeader>
                            <CardContent className="p-4 pt-0">
                              <h4 className="font-medium">프로젝트 {project}</h4>
                              <p className="text-sm text-muted-foreground">프로젝트 설명이 여기에 표시됩니다.</p>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </TabsContent>
                    <TabsContent value="skills" className="space-y-4 pt-4">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium">기술 스택</h3>
                        <Button size="sm">기술 추가</Button>
                      </div>
                      <div className="space-y-4">
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <div className="text-sm font-medium">React</div>
                            <div className="text-sm">숙련도: 상</div>
                          </div>
                          <div className="h-2 rounded-full bg-muted overflow-hidden">
                            <div className="h-full w-4/5 bg-primary"></div>
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <div className="text-sm font-medium">TypeScript</div>
                            <div className="text-sm">숙련도: 중</div>
                          </div>
                          <div className="h-2 rounded-full bg-muted overflow-hidden">
                            <div className="h-full w-3/5 bg-primary"></div>
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <div className="text-sm font-medium">Next.js</div>
                            <div className="text-sm">숙련도: 중</div>
                          </div>
                          <div className="h-2 rounded-full bg-muted overflow-hidden">
                            <div className="h-full w-3/5 bg-primary"></div>
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <div className="text-sm font-medium">Tailwind CSS</div>
                            <div className="text-sm">숙련도: 상</div>
                          </div>
                          <div className="h-2 rounded-full bg-muted overflow-hidden">
                            <div className="h-full w-4/5 bg-primary"></div>
                          </div>
                        </div>
                      </div>
                    </TabsContent>
                    <TabsContent value="education" className="space-y-4 pt-4">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium">교육 및 경력</h3>
                        <Button size="sm">항목 추가</Button>
                      </div>
                      <div className="space-y-4">
                        <Card>
                          <CardHeader>
                            <CardTitle>KDT 부트캠프</CardTitle>
                            <CardDescription>2023.01 - 2023.06</CardDescription>
                          </CardHeader>
                          <CardContent>
                            <p className="text-sm">
                              웹 개발 집중 과정을 수료하였으며, 프론트엔드 개발에 중점을 두었습니다. 팀 프로젝트를 통해
                              실무 경험을 쌓았습니다.
                            </p>
                          </CardContent>
                        </Card>
                        <Card>
                          <CardHeader>
                            <CardTitle>OO 대학교</CardTitle>
                            <CardDescription>2018.03 - 2022.02</CardDescription>
                          </CardHeader>
                          <CardContent>
                            <p className="text-sm">
                              컴퓨터 공학 학사 학위를 취득하였습니다. 알고리즘, 자료구조, 웹 개발 등의 과목을
                              수강하였습니다.
                            </p>
                          </CardContent>
                        </Card>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
      <footer className="border-t py-6">
        <div className="container flex flex-col items-center justify-center gap-4 text-center">
          <p className="text-sm text-muted-foreground">© 2025 TalentConnect. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
