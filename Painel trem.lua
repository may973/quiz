local player = game.Players.LocalPlayer
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "PainelTremBala"
ScreenGui.Parent = player:WaitForChild("PlayerGui")

-- Frame principal
local Frame = Instance.new("Frame")
local UIListLayout = Instance.new("UIListLayout")
local Titulo = Instance.new("TextLabel")
local Fechar = Instance.new("TextButton")
local Minimizar = Instance.new("TextButton")
local Pesquisa = Instance.new("TextBox")
local JogadoresScroll = Instance.new("ScrollingFrame")
local JogadoresLayout = Instance.new("UIListLayout")

Frame.Parent = ScreenGui
Frame.BackgroundColor3 = Color3.fromRGB(0, 0, 0)
Frame.Size = UDim2.new(0, 320, 0, 460)
Frame.Position = UDim2.new(0.05, 0, 0.25, 0)
Frame.Active = true
Frame.Draggable = true

-- Título
Titulo.Parent = Frame
Titulo.Size = UDim2.new(1, -40, 0, 40)
Titulo.Position = UDim2.new(0, 5, 0, 0)
Titulo.BackgroundTransparency = 1
Titulo.Text = "Painel Trem Bala"
Titulo.TextColor3 = Color3.fromRGB(255, 255, 255)
Titulo.TextScaled = true
Titulo.Font = Enum.Font.SourceSansBold
Titulo.TextXAlignment = Enum.TextXAlignment.Left

-- Botão Fechar
Fechar.Parent = Frame
Fechar.Size = UDim2.new(0, 30, 0, 30)
Fechar.Position = UDim2.new(1, -35, 0, 5)
Fechar.Text = "X"
Fechar.TextColor3 = Color3.fromRGB(255, 50, 50)
Fechar.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
Fechar.Font = Enum.Font.SourceSansBold
Fechar.TextScaled = true
Fechar.MouseButton1Click:Connect(function()
    ScreenGui:Destroy()
end)

-- Botão Minimizar
Minimizar.Parent = Frame
Minimizar.Size = UDim2.new(0, 30, 0, 30)
Minimizar.Position = UDim2.new(1, -70, 0, 5)
Minimizar.Text = "🔽"
Minimizar.TextColor3 = Color3.fromRGB(255, 255, 0)
Minimizar.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
Minimizar.Font = Enum.Font.SourceSansBold
Minimizar.TextScaled = true
local minimizado = false
Minimizar.MouseButton1Click:Connect(function()
    minimizado = not minimizado
    if minimizado then
        Frame.Size = UDim2.new(0, 320, 0, 50)
        JogadoresScroll.Visible = false
        Pesquisa.Visible = false
        Minimizar.Text = "🔼"
    else
        Frame.Size = UDim2.new(0, 320, 0, 460)
        JogadoresScroll.Visible = true
        Pesquisa.Visible = true
        Minimizar.Text = "🔽"
    end
end)

-- Barra de pesquisa
Pesquisa.Parent = Frame
Pesquisa.Size = UDim2.new(1, -10, 0, 30)
Pesquisa.Position = UDim2.new(0, 5, 0, 45)
Pesquisa.PlaceholderText = "Pesquisar jogador..."
Pesquisa.Text = ""
Pesquisa.TextScaled = true
Pesquisa.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
Pesquisa.TextColor3 = Color3.fromRGB(255, 255, 255)
Pesquisa.Font = Enum.Font.SourceSans

-- Lista de jogadores
JogadoresScroll.Parent = Frame
JogadoresScroll.Size = UDim2.new(1, -10, 1, -85)
JogadoresScroll.Position = UDim2.new(0, 5, 0, 80)
JogadoresScroll.CanvasSize = UDim2.new(0, 0, 0, 0)
JogadoresScroll.ScrollBarThickness = 8
JogadoresScroll.BackgroundColor3 = Color3.fromRGB(20, 20, 20)

JogadoresLayout.Parent = JogadoresScroll
JogadoresLayout.SortOrder = Enum.SortOrder.LayoutOrder

-- Tabela para Loop Kill
local loopKills = {}

-- Funções de ação
local function teleportTo(j)
    local char = player.Character
    if char and char:FindFirstChild("HumanoidRootPart") and j.Character and j.Character:FindFirstChild("HumanoidRootPart") then
        char.HumanoidRootPart.CFrame = j.Character.HumanoidRootPart.CFrame + Vector3.new(2,0,2)
    end
end

local function killPlayer(j)
    if j.Character and j.Character:FindFirstChild("Humanoid") then
        j.Character.Humanoid.Health = 0
    end
end

local function freezePlayer(j)
    if j.Character then
        for _, part in ipairs(j.Character:GetDescendants()) do
            if part:IsA("BasePart") then
                part.Anchored = true
            end
        end
    end
end

local function bringPlayer(j)
    local char = player.Character
    if char and char:FindFirstChild("HumanoidRootPart") and j.Character and j.Character:FindFirstChild("HumanoidRootPart") then
        j.Character.HumanoidRootPart.CFrame = char.HumanoidRootPart.CFrame + Vector3.new(3,0,0)
    end
end

local function flingPlayer(j)
    if j.Character and j.Character:FindFirstChild("HumanoidRootPart") then
        j.Character.HumanoidRootPart.Velocity = Vector3.new(9999,9999,9999)
    end
end

-- Loop Kill Toggle
local function toggleLoopKill(j)
    if loopKills[j] then
        loopKills[j] = nil
    else
        loopKills[j] = true
        task.spawn(function()
            while loopKills[j] do
                killPlayer(j)
                task.wait(1)
            end
        end)
    end
end

-- Criar submenu
local function abrirMenu(j, botao)
    local menu = Instance.new("Frame")
    menu.Size = UDim2.new(0,150,0,160)
    menu.Position = UDim2.new(0,botao.AbsolutePosition.X,0,botao.AbsolutePosition.Y+30)
    menu.BackgroundColor3 = Color3.fromRGB(30,30,30)
    menu.Parent = ScreenGui

    local function criarBotao(txt, ordem, func)
        local b = Instance.new("TextButton")
        b.Size = UDim2.new(1,0,0,30)
        b.Position = UDim2.new(0,0,0,(ordem-1)*30)
        b.Text = txt
        b.TextColor3 = Color3.fromRGB(255,255,255)
        b.BackgroundColor3 = Color3.fromRGB(50,50,50)
        b.TextScaled = true
        b.Parent = menu
        b.MouseButton1Click:Connect(function()
            func()
        end)
    end

    criarBotao("Teleportar",1,function() teleportTo(j) end)
    criarBotao("Kill",2,function() killPlayer(j) end)
    criarBotao("Freeze",3,function() freezePlayer(j) end)
    criarBotao("Loop Kill",4,function() toggleLoopKill(j) end)
    criarBotao("Bring",5,function() bringPlayer(j) end)
    criarBotao("Fling",6,function() flingPlayer(j) end)

    -- Fechar menu se clicar fora
    task.spawn(function()
        local uis = game:GetService("UserInputService")
        local con; con = uis.InputBegan:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                menu:Destroy()
                con:Disconnect()
            end
        end)
    end)
end

-- Função para adicionar jogador na lista
local function adicionarJogador(j)
    local botao = Instance.new("TextButton")
    botao.Size = UDim2.new(1, -5, 0, 30)
    botao.Text = j.Name
    botao.TextScaled = true
    botao.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    botao.TextColor3 = Color3.fromRGB(255, 255, 255)
    botao.Parent = JogadoresScroll
    botao.MouseButton1Click:Connect(function()
        abrirMenu(j, botao)
    end)
end

-- Atualizar lista
local function atualizarLista()
    JogadoresScroll:ClearAllChildren()
    JogadoresLayout.Parent = JogadoresScroll
    local jogadores = game.Players:GetPlayers()
    table.sort(jogadores, function(a, b) return a.Name:lower() < b.Name:lower() end)
    for _, j in ipairs(jogadores) do
        if j.Name:lower():find(Pesquisa.Text:lower()) then
            adicionarJogador(j)
        end
    end
    JogadoresScroll.CanvasSize = UDim2.new(0, 0, 0, (#JogadoresScroll:GetChildren() - 1) * 35)
end

-- Eventos
Pesquisa:GetPropertyChangedSignal("Text"):Connect(atualizarLista)
game.Players.PlayerAdded:Connect(atualizarLista)
game.Players.PlayerRemoving:Connect(atualizarLista)

-- Inicializar
atualizarLista()
